%global use_git 0
%global use_layers 1

%global commit  fbb866778e513752444f1bfd6a3fea3e3f4158b1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global srcname Vulkan-LoaderAndValidationLayers

%if 0%{?use_layers}
%global commit1 81cd764b5ffc475bc73f1fb35f75fd1171bb2343
%global srcname1 glslang

%global commit2 923a4596b44831a07060df45caacb522613730c9
%global srcname2 SPIRV-Tools

%global commit3 33d41376d378761ed3a4c791fc4b647761897f26
%global srcname3 SPIRV-Headers
%endif

Name:           vulkan
Version:        1.0.30.0
%if 0%{?use_git}
Release:        0.2.git%{shortcommit}%{?dist}
%else
Release:        2%{?dist}
%endif
Summary:        Vulkan loader and validation layers

License:        ASL 2.0
URL:            https://github.com/KhronosGroup

%if 0%{?use_git}
Source0:        %url/%{srcname}/archive/%{commit}.tar.gz#/%{srcname}-%{commit}.tar.gz
%else
Source0:        %url/%{srcname}/archive/sdk-%{version}.tar.gz#/%{srcname}-sdk-%{version}.tar.gz
%endif
%if 0%{?use_layers}
Source1:        %url/%{srcname1}/archive/%{commit1}.tar.gz#/%{srcname1}-%{commit1}.tar.gz
Source2:        %url/%{srcname2}/archive/%{commit2}.tar.gz#/%{srcname2}-%{commit2}.tar.gz
Source3:        %url/%{srcname3}/archive/%{commit3}.tar.gz#/%{srcname3}-%{commit3}.tar.gz
%else
Source4:        https://raw.githubusercontent.com/KhronosGroup/glslang/master/SPIRV/spirv.hpp
%endif
# All patches taken from ajax's repo
# https://github.com/nwnk/Vulkan-LoaderAndValidationLayers/tree/sdk-1.0.3-fedora
Patch0:         0003-layers-Don-t-set-an-rpath.patch
Patch1:         0004-layers-Install-to-CMAKE_INSTALL_LIBDIR.patch
Patch2:         0005-loader-Add-install-rule.patch
Patch3:         0008-demos-Don-t-build-tri-or-cube.patch

# Upstream patches
Patch4:         5338f69a0a3dcc8527d81ca5f936b0e066a3d7f7.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  /usr/bin/chrpath
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  python3
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)

Requires:       vulkan-filesystem = %{version}-%{release}

%description
Vulkan is a new generation graphics and compute API that provides
high-efficiency, cross-platform access to modern GPUs used in a wide variety of
devices from PCs and consoles to mobile phones and embedded platforms.

This package contains the reference ICD loader and validation layers for
Vulkan.

%package devel
Summary:        Vulkan development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for Vulkan applications.

%package filesystem
Summary:        Vulkan filesystem package
BuildArch:      noarch

%description filesystem
Filesystem for Vulkan.

%prep
%if 0%{?use_git}
%autosetup -p1 -n %{srcname}-%{commit}
%else
%autosetup -p1 -n %{srcname}-sdk-%{version}
%endif
%if 0%{?use_layers}
mkdir -p build/ external/glslang/build/install external/spirv-tools/build/ external/spirv-tools/external/spirv-headers
tar -xf %{SOURCE1} -C external/glslang --strip 1
tar -xf %{SOURCE2} -C external/spirv-tools --strip 1
tar -xf %{SOURCE3} -C external/spirv-tools/external/spirv-headers --strip 1
# fix spurious-executable-perm
chmod 0644 README.md
chmod 0644 external/glslang/SPIRV/spirv.hpp
%else
mkdir -p build/
cp %{SOURCE4} .
%endif
# fix wrong-script-end-of-line-encoding
sed -i 's/\r//' README.md

# sigh inttypes
sed -i 's/inttypes.h/cinttypes/' layers/*.{cpp,h} *.py

%build
%if 0%{?use_layers}
pushd external/glslang/build/
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS ; 
CXXFLAGS="$RPM_OPT_FLAGS" ; export CXXFLAGS ; 
LDFLAGS="$RPM_LD_FLAGS" ; export LDFLAGS ;
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON ..
%make_build
make install
popd
pushd external/spirv-tools/build/
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON ..
%make_build
popd
%endif
pushd build/
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=yes \
       -DCMAKE_SKIP_RPATH:BOOL=yes \
       -DBUILD_VKJSON=OFF \
       -DBUILD_WSI_WAYLAND_SUPPORT=ON \
%if 0%{?use_layers}
 ..
%else
       -DGLSLANG_SPIRV_INCLUDE_DIR=./ \
       -DBUILD_TESTS=OFF \
       -DBUILD_LAYERS=OFF ..
%endif
%make_build
popd

%install
pushd build/
%{make_install}
popd

mkdir -p %{buildroot}%{_includedir}
%if 0%{?use_layers}
mkdir -p %{buildroot}%{_datadir}/vulkan/implicit_layer.d
mv %{buildroot}%{_sysconfdir}/vulkan/explicit_layer.d/ %{buildroot}%{_datadir}/vulkan/
%endif

# remove RPATH
chrpath -d %{buildroot}%{_bindir}/vulkaninfo

cp -ai include/vulkan %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_sysconfdir}/vulkan/icd.d

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.txt COPYRIGHT.txt
%doc README.md CONTRIBUTING.md
%{_bindir}/vulkaninfo
%if 0%{?use_layers}
%{_datadir}/vulkan/explicit_layer.d/*.json
%{_libdir}/libVkLayer_*.so
%endif
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files filesystem
%dir %{_sysconfdir}/vulkan
%dir %{_sysconfdir}/vulkan/icd.d
%if 0%{?use_layers}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/explicit_layer.d
%dir %{_datadir}/%{name}/implicit_layer.d
%endif

%changelog
* Mon Jan 09 2017 sulit - 1.0.30.0-2
- init build for isoft

