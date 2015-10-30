%define debug_package %{nil}

Summary: MPlayer, the Movie Player for Linux.
Name: mplayer
Version: 1.2
License: GPL
Release: 13 
Source0: http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{version}.tar.xz

Source1: mplayer.conf
Patch0: mplayer-add-missing-lib.patch 

Requires:pulseaudio-libs
BuildRequires: yasm
BuildRequires: pulseaudio-libs-devel
BuildRequires: mesa-libGL-devel 
BuildRequires: mesa-libEGL-devel 
BuildRequires: libX11-devel, libXext-devel, libXinerama-devel, libXScrnSaver-devel, libXv-devel
BuildRequires: a52dec-devel, libass-devel, libbluray-devel, libcdio-devel, libcdio-paranoia-devel
BuildRequires: libdv-devel, enca-devel, faac-devel, faad2-devel, fribidi-devel, enca-devel, libjpeg-turbo-devel
BuildRequires: libmad-devel, ncurses-devel, libogg-devel, libpng-devel, libspeex-devel, libvdpau-devel, x264-devel
BuildRequires: libvpx-devel, xvidcore-devel
BuildRequires: fontconfig-devel, freetype-devel
BuildRequires: alsa-lib-devel

%description
MPlayer is a movie player. It plays most video formats as well as DVDs.
Its big feature is the wide range of supported output drivers. There are also
nice antialiased shaded subtitles and OSD.

%prep
%setup -q -n MPlayer-%{version}
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir}/mplayer \
    --confdir=%{_sysconfdir}/mplayer \
    --mandir=%{_mandir} \
    --codecsdir=/usr/lib/win32 \
    --enable-runtime-cpudetection \
    --disable-qtx \
    --enable-fbdev \
    --enable-tdfxfb \
    --enable-pulse \
    --enable-vm \
    --enable-x11 \
    --enable-xmga \
    --language=en \
    --disable-gui \
    --enable-mga  \
    --enable-menu \
    --enable-dynamic-plugins \
    --enable-freetype \
    --disable-sdl \
    --disable-ivtv \
    --disable-arts \
    --enable-vdpau \
    --disable-mp3lame \
    --disable-mp3lame-lavc

make %{?_smp_mflags}
%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 etc/input.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/codecs.conf %{buildroot}%{_sysconfdir}/%{name}

mkdir -p $RPM_BUILD_ROOT/etc/mplayer
cp -r %{SOURCE1} $RPM_BUILD_ROOT/etc/mplayer 
rm -rf $RPM_BUILD_ROOT/usr/bin/gmplayer
rm -rf $RPM_BUILD_ROOT/usr/share/applications
rm -rf $RPM_BUILD_ROOT/usr/share/pixmaps
rm -rf $RPM_BUILD_ROOT/usr/share/mplayer

%clean
rm -rf $RPM_BUILD_ROOT 
rm -rf $RPM_BUILD_DIR/%{name}-%{version} 
 

%files
%defattr(-, root, root, 755)
%dir %{_sysconfdir}/mplayer
%{_sysconfdir}/mplayer/*.conf
%{_bindir}/mencoder
%{_bindir}/mplayer
%{_mandir}/man1/mencoder.1.gz
%{_mandir}/man1/mplayer.1.gz

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.2-13
- Rebuild

* Mon Oct 05 2015 Cjacker <cjacker@foxmail.com>
- update to 1.2

* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- update to 1.1.1

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

