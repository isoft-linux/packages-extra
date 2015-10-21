Name: mpv	
Version: 0.11.0
Release: 2 
Summary: a free, open source, and cross-platform media player

License: GPLv2
URL: http://mpv.io/
Source0: %{name}-%{version}.tar.gz

BuildRequires: waf
BuildRequires: libX11-devel, libXt-devel, libXext-devel, libXScrnSaver-devel
BuildRequires: pulseaudio-libs-devel, alsa-lib-devel
BuildRequires: libcdio-devel, ffmpeg-devel, libguess-devel, libass-devel 
BuildRequires: libbluray-devel, libdvdread-devel, libdvdnav-devel 
BuildRequires: enca-devel, lcms2-devel
BuildRequires: libva-devel, libvdpau-devel
BuildRequires: luajit-devel
 
Requires: luajit	

%description
%{summary}

%package -n libmpv
Summary:        mpv client library
Group:          System Environment/Libraries

%description -n libmpv
mpv client library.

%package -n libmpv-devel
Summary:        Development files for lib%{name}
Group:          Development/Libraries
Requires:       lib%{name} = %{version}-%{release}

%description -n libmpv-devel
The lib%{name}-devel package contains libraries and header files for
developing applications that use lib%{name}.


%prep
%setup -q

%build
waf configure \
    --prefix=%{_prefix} \
    --confdir=%{_sysconfdir}/mpv \
    --datadir=%{_datadir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/mpv \
    --disable-libsmbclient \
    --disable-rubberband \
    --disable-vapoursynth \
    --disable-vapoursynth-lazy \
    --disable-sdl2 \
    --disable-sdl1 \
    --disable-oss-audio \
    --disable-openal \
    --disable-egl-x11 \
    --disable-jpeg \
    --disable-libavresample \
    --enable-lua \
    --lua=luajit \
    --enable-shm \
    --enable-libguess \
    --enable-libass \
    --enable-libass-osd \
    --enable-encoding \
    --enable-libbluray \
    --enable-dvdread \
    --enable-dvdnav \
    --enable-cdda \
    --enable-enca \
    --enable-lcms2 \
    --enable-libswresample \
    --enable-libavfilter \
    --enable-libavdevice \
    --enable-pulse \
    --enable-alsa \
    --enable-wayland \
    --enable-x11 \
    --enable-xss \
    --enable-xext \
    --enable-xv \
    --enable-xinerama \
    --enable-xrandr \
    --enable-gl-x11 \
    --enable-gl-wayland \
    --enable-vdpau \
    --enable-vdpau-gl-x11 \
    --enable-vaapi \
    --enable-vaapi-vpp \
    --enable-vaapi-glx \
    --enable-drm \
    --enable-gl \
    --enable-vaapi-hwaccel \
    --enable-vdpau-hwaccel \
    --enable-tv \
    --enable-tv-v4l2 \
    --enable-libv4l2 \
    --enable-libmpv-shared

waf build

%install
waf install --destdir=%{buildroot}

#hide menu item.
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/mpv.desktop

%files
%{_sysconfdir}/mpv/encoding-profiles.conf
%{_bindir}/mpv
%{_mandir}/man1/mpv.1*
%{_datadir}/icons/hicolor/*/apps/mpv.*
%{_datadir}/applications/mpv.desktop
%{_docdir}/mpv/

%files -n libmpv
%{_libdir}/libmpv.so.*

%files -n libmpv-devel
%{_libdir}/libmpv.so
%{_includedir}/mpv
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to 0.11.0

* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- add shared library and development package.
