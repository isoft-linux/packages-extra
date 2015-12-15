%global realname wxGTK

Name:           wxGTK28
Version:        2.8.12
Release:        21%{?dist}
Summary:        GTK2 port of the wxWidgets GUI library
License:        wxWidgets
URL:            http://www.wxwidgets.org/
Source0:        http://downloads.sourceforge.net/wxwindows/%{realname}-%{version}.tar.bz2
Patch0:         %{realname}-2.8.12-test.patch
# remove abort when ABI check fails
Patch1:         %{realname}-2.8.12-abicheck.patch

BuildRequires:  gtk2-devel, zlib-devel >= 1.1.4
BuildRequires:  libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  expat-devel, SDL-devel
BuildRequires:  libGL-devel, libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  gstreamer-devel >= 0.10, gstreamer-plugins-base-devel >= 0.10
BuildRequires:  GConf2-devel
BuildRequires:  autoconf, gettext
BuildRequires:  cppunit-devel

Requires: %{name}-common = %{version}-%{release}
 

Provides: bundled(scintilla) = 1.70
#provies these package names.
Provides: %{name}-gl = %{version}-%{release}
Provides: %{name}-media = %{version}-%{release}
Provides: wxGTK = %{version}-%{release}
Provides: wxGTK-gl = %{version}-%{release}
Provides: wxGTK-media = %{version}-%{release}
Provides: wxBase = %{version}-%{release}

%description
wxWidgets/GTK2 is the GTK2 port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.

%package common
Summary: Common files for the wxGTK2 library

%description common
This package common files for the wxGTK2 library.
Such as translations.

%package common-devel
Summary: Common development files for the wxGTK2 library
Requires: bakefile

%description common-devel
This package common include files needed to link with the wxGTK2 library.

%package shared-devel
Summary:Development files to link with the wxGTK2 shared library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common-devel = %{version}-%{release}
Requires: %{name}-gl = %{version}-%{release}
Requires: %{name}-media = %{version}-%{release}
Requires: gtk2-devel
Requires: libGL-devel, libGLU-devel
Requires: bakefile
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

Provides: wxGTK-devel = %{name}-%{version}

%description shared-devel
This package include files needed to link with the wxGTK2 shared library.

%package  static-devel
Summary: Development files to link with the wxGTK2 static library
Requires: %{name}-common-devel = %{version}-%{release}
Requires: gtk2-devel
Requires: libGL-devel, libGLU-devel
Requires: bakefile
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives


%description static-devel
This package include files needed to link with the wxGTK2 static library.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1 -b .test
%patch1 -p1 -b .abicheck

sed -i -e 's|/usr/lib\b|%{_libdir}|' wx-config.in configure

# fix plugin dir for 64-bit
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

# fix permissions for sources
chmod a-x include/wx/{msgout.h,dcgraph.h,graphics.h}
chmod a-x src/common/msgout.cpp


# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).

%define common_args --with-opengl --with-sdl --without-gnomeprint --disable-optimise --enable-debug_info --enable-intl --enable-unicode --enable-no_deps --disable-rpath --enable-geometry --enable-graphics_ctx --enable-sound --enable-mediactrl --enable-display --enable-timer --enable-compat24 --disable-catch_segvs

%build
export GDK_USE_XFT=1

# this code dereferences type-punned pointers like there's no tomorrow.
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC"
CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC"


#shared library
mkdir shared-build
pushd shared-build
ln -s ../configure .
%configure \
  --enable-shared \
  --enable-soname \
  %{common_args} 

make %{?_smp_mflags}
make %{?_smp_mflags} -C contrib/src/stc
make %{?_smp_mflags} -C contrib/src/ogl
make %{?_smp_mflags} -C contrib/src/gizmos
make %{?_smp_mflags} -C contrib/src/svg
popd

#static library
mkdir static-build
pushd static-build
ln -s ../configure .
%configure \
  --disable-shared \
  %{common_args} 

make %{?_smp_mflags}
make %{?_smp_mflags} -C contrib/src/stc
make %{?_smp_mflags} -C contrib/src/ogl
make %{?_smp_mflags} -C contrib/src/gizmos
make %{?_smp_mflags} -C contrib/src/svg
popd 


#locale files
make %{?_smp_mflags} -C locale allmo

%install
#install shared library
pushd shared-build
%makeinstall

%makeinstall -C contrib/src/stc
%makeinstall -C contrib/src/ogl
%makeinstall -C contrib/src/gizmos
%makeinstall -C contrib/src/svg
popd

#install static library
pushd static-build
%makeinstall

%makeinstall -C contrib/src/stc
%makeinstall -C contrib/src/ogl
%makeinstall -C contrib/src/gizmos
%makeinstall -C contrib/src/svg
popd


%find_lang wxstd
%find_lang wxmsw
cat wxmsw.lang >> wxstd.lang

#fix wx-config link destination.
#wx-config support using args to switch build profile, even so, we also use alternatives to manage it.

rm -f $RPM_BUILD_ROOT%{_bindir}/wx-config
ln -sf /etc/alternatives/wx-config $RPM_BUILD_ROOT%{_bindir}/wx-config

#fix a missing DSO in static wx-config
sed -i 's/-lXinerama/-lXinerama -lX11/g' %{buildroot}%{_libdir}/wx/config/gtk2-unicode-release-static-2.8

%check
pushd shared-build
pushd tests
make test
popd
popd

pushd static-build
pushd tests
make test
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post shared-devel
%{_sbindir}/update-alternatives --install %{_bindir}/wx-config \
   wx-config %{_libdir}/wx/config/gtk2-unicode-release-2.8 30

%preun shared-devel
if [ $1 = 0 ]; then
   %{_sbindir}/update-alternatives --auto wx-config
fi

%post static-devel
%{_sbindir}/update-alternatives --install %{_bindir}/wx-config \
   wx-config %{_libdir}/wx/config/gtk2-unicode-release-static-2.8 50 

%preun static-devel
if [ $1 = 0 ]; then
   %{_sbindir}/update-alternatives --auto wx-config
fi

%files 
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_gtk2u_adv-*.so.*
%{_libdir}/libwx_gtk2u_aui-*.so.*
%{_libdir}/libwx_gtk2u_core-*.so.*
%{_libdir}/libwx_gtk2u_gizmos-*.so.*
%{_libdir}/libwx_gtk2u_gizmos_xrc*.so.*
%{_libdir}/libwx_gtk2u_html-*.so.*
%{_libdir}/libwx_gtk2u_ogl-*.so.*
%{_libdir}/libwx_gtk2u_qa-*.so.*
%{_libdir}/libwx_gtk2u_richtext-*.so.*
%{_libdir}/libwx_gtk2u_stc-*.so.*
%{_libdir}/libwx_gtk2u_svg-*.so.*
%{_libdir}/libwx_gtk2u_xrc-*.so.*
#wxbase
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.*
%{_libdir}/libwx_baseu_xml-*.so.*
#gl
%{_libdir}/libwx_gtk2u_gl-*.so.*
#media
%{_libdir}/libwx_gtk2u_media-*.so.*


#common package only contains translations.
%files common -f wxstd.lang

%files common-devel
%{_bindir}/wx-config
%{_bindir}/wxrc*
%{_includedir}/wx-2.8
%dir %{_libdir}/wx
%dir %{_libdir}/wx/include
%{_datadir}/aclocal/*
%{_datadir}/bakefile/presets/*

%files shared-devel
%{_libdir}/libwx_*.so
%{_libdir}/wx/config/gtk2-unicode-release-2.8
%{_libdir}/wx/include/gtk2-unicode-release-2.8

%files static-devel
%{_libdir}/libwx_*.a
%{_libdir}/libwxregexu-*.a
%{_libdir}/wx/config/gtk2-unicode-release-static-2.8
%{_libdir}/wx/include/gtk2-unicode-release-static-2.8

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.8.12-21
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 2.8.12-20
- Initial build

