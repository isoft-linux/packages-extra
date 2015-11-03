%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt %{?*} >/dev/null 2>&1 || : \
%{nil}


Summary: A Windows 16/32/64 bit emulator
Name: wine 
Version: 1.7.54
Release: 2 
License: GPL
URL: https://www.winehq.org
Source0: http://mirrors.ibiblio.org/wine/source/1.7/%{name}-%{version}.tar.bz2
Source1: wine-staging-%{version}.tar.gz

Source2: wine.systemd

Patch0: wine-fix-xim-cursor-follow.patch

Patch10: wine-cjk.patch
# temporary workaround for GCC 5.0 optimization regressions
Patch11: wine-gcc5.patch
#patch 12 is patch11 rebased with wine-staging.
Patch12: wine-gcc5-with-wine-staging.patch

Patch13: wine-disable-menubuilder-to-avoid-pollute-the-system-mime-and-menu.patch

ExclusiveArch: %{ix86} x86_64


BuildRequires: bison
BuildRequires: flex
BuildRequires: autoconf
BuildRequires: desktop-file-utils
BuildRequires: alsa-lib-devel
BuildRequires: freeglut-devel
BuildRequires: lcms2-devel
BuildRequires: libieee1284-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libstdc++-devel
BuildRequires: libusb-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: ncurses-devel
BuildRequires: opencl-headers
BuildRequires: openldap-devel
BuildRequires: sane-backends-devel
BuildRequires: zlib-devel
BuildRequires: freetype-devel
BuildRequires: libgphoto2-devel
BuildRequires: libpcap-devel
BuildRequires: gtk3-devel
BuildRequires: opencl-headers
BuildRequires: libva-devel 
BuildRequires: libX11-devel
BuildRequires: mesa-libGL-devel libGLU-devel
BuildRequires: libXxf86dga-devel libXxf86vm-devel
BuildRequires: libXrandr-devel libXrender-devel
BuildRequires: libXext-devel
BuildRequires: libXinerama-devel
BuildRequires: libXcomposite-devel
BuildRequires: fontconfig-devel
BuildRequires: giflib-devel
BuildRequires: cups-devel
BuildRequires: libXmu-devel
BuildRequires: libXi-devel
BuildRequires: libXcursor-devel
BuildRequires: dbus-devel
BuildRequires: gnutls-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libv4l-devel
BuildRequires: ImageMagick-devel
BuildRequires: libtiff-devel
BuildRequires: gettext-devel
BuildRequires: libexif-devel
BuildRequires: libgphoto2-devel
BuildRequires: libmpg123-devel
BuildRequires: ocl-icd-devel
BuildRequires: openal-devel


%description
A Windows 16/32/64 bit emulator

%package devel
Summary: Libraries, includes, etc to develop applications with wine emulators
Requires: %{name} = %{version}-%{release}

%description devel
Libraries and include files that can be used to develop applications with wine emulators.

%prep
%setup -q -a1 
pushd wine-staging-%{version}/patches
./patchinstall.sh DESTDIR=`pwd`/../.. --all
popd

%patch0 -p1
#%patch1 -p1

%patch10 -p1
#%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
#fix gcc5 issue.
export TEMP_CFLAGS="`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/'`"
export CFLAGS="`echo $TEMP_CFLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

export CC=cc
export CXX=c++

#wine staging required.
autoreconf -ivf

%configure \
%ifarch x86_64 
    --disable-win16 \
    --enable-win64 \
%endif
    --with-pulse \
    --with-cms \
    --with-cups \
    --with-curses \
    --with-dbus \
    --with-fontconfig \
    --with-freetype \
    --with-gettext \
    --with-glu \
    --with-gnutls \
    --without-gstreamer \
    --without-hal \
    --with-jpeg \
    --with-netapi \
    --with-opengl \
    --with-openal \
    --with-opencl \
    --with-png \
    --with-sane \
    --with-tiff \
    --with-v4l \
    --with-xcomposite \
    --with-xcursor \
    --with-xinerama \
    --with-xml \
    --with-xrandr \
    --with-x \
    --with-gtk3 \
    --with-va \
    --without-ldap

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#make links
pushd $RPM_BUILD_ROOT/%{_bindir}
ln -s wine64 wine
ln -s wine64-preloader wine-preloader
popd

#install binfmt.d file
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf


#remove all fonts shipped with wine
#rm -rf $RPM_BUILD_ROOT/usr/share/wine/fonts


%clean
rm -rf $RPM_BUILD_ROOT

%post
%binfmt_apply wine.conf

%postun
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi


%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/*/man1/*
%{_datadir}/applications/wine.desktop
%dir %{_datadir}/wine
%{_datadir}/wine
%{_bindir}/*
%{_libdir}/libwine.so.*
%{_libdir}/wine/*
%{_binfmtdir}/wine.conf

%exclude %{_bindir}/wineg++
%exclude %{_bindir}/widl
%exclude %{_bindir}/function_grep.pl
%exclude %{_bindir}/wrc
%exclude %{_bindir}/winebuild
%exclude %{_bindir}/winecpp
%exclude %{_bindir}/winegcc
%exclude %{_bindir}/wmc


%files devel
%defattr(-, root,root)
%{_bindir}/wineg++
%{_bindir}/widl
%{_bindir}/function_grep.pl
%{_bindir}/wrc
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winegcc
%{_bindir}/wmc
%{_libdir}/libwine.so
%dir %{_includedir}/wine
%{_includedir}/wine/*

%changelog
* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 1.7.54-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.7.53-4
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 1.7.53-3
- update

* Mon Oct 05 2015 Cjacker <cjacker@foxmail.com>
- update to 1.7.52

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- enable wine-staging.
- enable gtk3 style.

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to 1.7.49
