#set to 1 to use clang.
%global _build_with_clang 1 

Name:	    webkitgtk4
Version:    2.12.3
Release:    1
Summary:    GTK Port of WebKit

License:	MIT
URL:	    http://www.webkitgtk.org
Source0:    webkitgtk-%{version}.tar.xz

BuildRequires: cmake ninja-build make
BuildRequires: libXt-devel
BuildRequires: bison flex gperf perl python ruby pkgconfig
BuildRequires: gettext
BuildRequires: cairo-devel fontconfig-devel freetype-devel
BuildRequires: gtk3-devel
BuildRequires: harfbuzz-devel
BuildRequires: libicu-devel libjpeg-turbo-devel libsoup-devel libxml2-devel libxslt-devel
BuildRequires: zlib-devel libpng-devel sqlite-devel
BuildRequires: atk-devel libwebp-devel at-spi2-core-devel 
BuildRequires: pkgconfig(gl) pkgconfig(egl) pkgconfig(glesv2)
BuildRequires: libsecret-devel geoclue2-devel
BuildRequires: gobject-introspection-devel
#yes, still need it.
BuildRequires: gtk2-devel
BuildRequires: enchant-devel
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: libX11-devel libXext-devel
BuildRequires: pkgconfig(wayland-client) pkgconfig(wayland-egl) pkgconfig(wayland-server)
BuildRequires: libnotify-devel hyphen-devel hunspell-devel

BuildRequires: chrpath

%if %_build_with_clang
BuildRequires: clang
%endif

%description
WebKit/GTK is a project aiming at porting WebKit to GTK library.

%package devel
Summary: Development files for %{name} 
Requires: %{name} = %{version}-%{release}

%description devel
The header files and libraries for %{name} 

%prep
%setup -q -n webkitgtk-%{version} 



%Build
#build it
mkdir -p build 
pushd build
%cmake \
    %if %_build_with_clang
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++  \
    %endif
    -DCMAKE_BUILD_TYPE=Release \
    -DPORT=GTK \
    -DCMAKE_SKIP_RPATH=ON \
    -DENABLE_GTKDOC=OFF \
    ..

make %{?_smp_mflags}
popd    

%install
pushd build
make install DESTDIR=%{buildroot}
popd


%files
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_libdir}/webkit2gtk-*/injected-bundle/libwebkit2gtkinjectedbundle.so
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_libdir}/girepository-?.?/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-?.?/*.gir
%{_datadir}/gtk-doc/html/*

%changelog
* Thu Jul 07 2016 zhouyang <yang.zhou@i-soft.com.cn> - 2.12.3-1
- Update
- disable gtkdoc for now.

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 2.10.3-3
- Update and rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.10.0-2
- Rebuild

