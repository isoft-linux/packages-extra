Name:    vlc
Summary: vlc video player
Version: 2.2.1
Release: 2 

License: LGPLv2+
Group:   System Environment/Libraries
URL:    http://www.videolan.org
Source0: http://get.videolan.org/vlc/2.2.1/vlc-%{version}.tar.xz
Patch0: vlc-lua-5.3.patch
Patch2: vlc-2.1.0-fix-libtremor-libs.patch
Patch3: vlc-9999-libva-1.2.1-compat.patch
Patch4: vlc-2.2.0-rdp-1.2.0.patch
Patch5: vlc-2.2.0-xcb_vdpau.patch
Patch6: vlc-2.1.0-TomWij-bisected-PA-broken-underflow.patch
Patch7: qt4-select.patch
Patch8: opencv-3.0.0.patch

BuildRequires: cmake
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: alsa-lib-devel
BuildRequires: libmtp-devel
BuildRequires: vcdimager-devel
BuildRequires: ffmpeg-devel
BuildRequires: xvidcore-devel
BuildRequires: qt4-devel
BuildRequires: lua-devel

#for update-desktop-database
Requires(pre): desktop-file-utils
#for gtk3-update-icon-cache
Requires(pre): gtk3

%description
vlc video player

%package -n libvlc
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries

%description -n libvlc
The package contains runtime libraries of VLC.

%package -n libvlc-devel
Summary: Development files for %{name}
Group:   Development/Libraries
Requires: libvlc = %{version}-%{release}

%description -n libvlc-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%package apidocs
Group: Development/Documentation
Summary: Grantlee API documentation
Requires: kde-filesystem
BuildArch: noarch
%description apidocs
This package includes the Grantlee API documentation in HTML
format for easy browsing.


%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p0

%build
#autoreconf -ivf
./bootstrap
%configure \
    --disable-httpd \
    --enable-vlm \
    --enable-dvdread \
    --enable-bluray \
    --enable-dvdnav \
    --disable-opencv \
    --disable-smbclient \
    --disable-sftp \
    --enable-v4l2 \
    --disable-gnomevfs \
    --enable-vcd \
    --enable-vcdx \
    --enable-libcddb \
    --enable-screen \
    --enable-xcb \
    --disable-vnc \
    --disable-freerdp \
    --enable-lua \
    --enable-realrtsp \
    --enable-ogg \
    --enable-mux_ogg \
    --enable-mad \
    --enable-avcodec \
    --enable-avformat \
    --enable-swscale \
    --enable-postproc \
    --enable-libva \
    --enable-faad \
    --enable-a52 \
    --enable-flac \
    --enable-vorbis \
    --disable-speex \
    --enable-theora \
    --enable-png \
    --enable-x264 \
    --enable-libass \
    --enable-gles2 \
    --with-x \
    --enable-xvideo \
    --disable-sdl \
    --disable-sdl-image \
    --enable-freetype \
    --enable-fribidi \
    --enable-fontconfig \
    --enable-svg \
    --enable-pulse \
    --enable-alsa \
    --disable-projectm \
    --enable-vdpau \
    --enable-taglib \
    --disable-ncurses \
    --disable-dca \
    --enable-qt=4 \
    --with-default-font=/usr/share/fonts/SourceHanSansCN-Normal.otf \
    --with-default-font-family="Source Han Sans CN" \
    --with-default-monospace-font=/usr/share/fonts/SourceHanSansCN-Normal.otf \
    --with-default-monospace-font-family="Source Han Sans CN"

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#this is for kf5 solid
mkdir -p %{buildroot}%{_datadir}/solid/actions/
mv %{buildroot}%{_datadir}/kde4/apps/solid/actions/*.desktop %{buildroot}%{_datadir}/solid/actions/
rm -rf %{buildroot}%{_datadir}/kde4

%find_lang vlc

%clean
rm -rf %{buildroot}


%post 
/sbin/ldconfig ||:
gtk3-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database -q ||:

%postun 
/sbin/ldconfig ||:
gtk3-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database -q ||:

%post -n libvlc -p /sbin/ldconfig
%postun -n libvlc -p /sbin/ldconfig

%files -f vlc.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/applications/vlc.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/*
%dir %{_datadir}/vlc
%{_datadir}/vlc/*
%{_libdir}/vlc/plugins/gui/*
%{_libdir}/vlc/lua/

%{_datadir}/solid/actions/*.desktop

%files -n libvlc
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%dir %{_libdir}/vlc
%{_libdir}/vlc/plugins/*
%{_libdir}/vlc/vlc-cache-gen
%{_libdir}/vlc/libvlc_vdpau.so*
%exclude %{_libdir}/vlc/plugins/gui/*


%files -n libvlc-devel
%defattr(-,root,root,-)
%dir %{_includedir}/vlc
%{_includedir}/vlc/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/vlc/libcompat.a
%dir %{_docdir}/vlc
%{_docdir}/vlc/*

%changelog
* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- back to qt4
- setup default fonts to support Chinese OSD/SubTitle.

* Sat Jul 18 2015 Cjacker <cjacker@foxmail.com>
- fix build with lua-5.3

* Tue Jul 14 2015 Cjacker <cjacker@foxmail.com>
- add solid actions for kf5
* Mon Jul 13 2015 Cjacker <cjacker@foxmail.com>
- rebuild with qt 5.5.0
