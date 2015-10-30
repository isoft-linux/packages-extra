Name:           libxine 
Summary:        A portable video/audio library for unix-like systems.
Version:        1.2.6
Release:        2 
License:        GPL
URL:            http://xinehq.de
Source:         http://xinehq.de/files/xine-lib-%{version}.tar.xz
Provides:       xine
Provides:       xine-lib
BuildRequires: ffmpeg-devel
BuildRequires: optipng
BuildRequires: SDL-devel
BuildRequires: a52dec-devel
BuildRequires: alsa-lib-devel
BuildRequires: faad2-devel
BuildRequires: ffmpeg-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: glib2-devel
BuildRequires: ImageMagick-devel
BuildRequires: libbluray-devel
BuildRequires: libflac-devel
BuildRequires: libGLU-devel
BuildRequires: libgomp
BuildRequires: libICE-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libmad-devel
BuildRequires: libmng-devel
BuildRequires: libmpcdec-devel
BuildRequires: libogg-devel
BuildRequires: libsmbclient-devel
BuildRequires: libSM-devel
BuildRequires: libspeex-devel
BuildRequires: libtheora-devel
BuildRequires: libv4l-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libvorbis-devel
BuildRequires: libvpx-devel
BuildRequires: libX11-devel
BuildRequires: libxcb-devel
BuildRequires: libXext-devel
BuildRequires: libXinerama-devel
BuildRequires: libXv-devel
BuildRequires: libXvMC-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: zlib-devel

%description
libxine is the beating heart of xine (a free gpl-licensed video player for
unix-like systems) which among others provides support for decoding (and
playing back) of many today available audio/video codecs, like mpeg-4 (DivX),
mpeg-2 (DVD, SVCD), mpeg-1 (VCD), Quicktime and RealMedia just to name a few.
This library contains (and uses) numerous processor specific optimizations to
provide a smooth playback and to minimize the overall demand of CPU power.

Don't hesitate to use libxine in your own projects as long as your usage
complies to the GPL. More information about GPL-license can be found at
http://www.gnu.org/licenses/gpl.html

%package devel
Summary:        Header files and documentation to develope programs with libxine.
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains header files and documentation required to develope
programs with libxine.

libxine is the beating heart of xine (a free gpl-licensed video player for
unix-like systems) which among others provides support for decoding (and
playing back) of many today available audio/video codecs, like mpeg-4 (DivX),
mpeg-2 (DVD, SVCD), mpeg-1 (VCD), Quicktime and RealMedia just to name a few.
This library contains (and uses) numerous processor specific optimizations to
provide a smooth playback and to minimize the overall demand of CPU power.

Don't hesitate to use libxine in your own projects as long as your usage
complies to the GPL. More information about GPL-license can be found at
http://www.gnu.org/licenses/gpl.html

%prep
%setup -q -n xine-lib-%{version}
%build
if [ ! -f configure ]; then
   NO_CONFIGURE=1 ./autogen.sh
fi

# currently we do not use %%configure as it seems to cause trouble with
# certain automake produced configure scripts - depending on automake version.
# Use BUILD_ARGS envvar to pass extra parameters to configure (like --enable-dha-mod/etc...)
#
./configure \
    --build=%{_target_platform} \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-w32-path=/usr/lib/win32 \
    --with-real-codecs-path=/usr/lib/win32 \
    --with-freetype \
    --with-pulseaudio \
    --disable-vcd \
    XCB_LIBS="-lxcb -lxcb-shape -lxcb-shm"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{?buildroot:%{buildroot}} LIBRARY_PATH=%{?buildroot:%{buildroot}}%{_libdir} install


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_bindir}/xine-list*
%{_mandir}/man1/xine-list-1.2.1.gz
%{_libdir}/*.so.*
%dir %{_libdir}/xine
%{_libdir}/xine/*
%dir %{_datadir}/xine-lib
%{_datadir}/xine-lib/*

%{_mandir}/man5/*

%{_datadir}/locale/*/*/*.mo


%files devel
%defattr(-, root, root, -)
%{_bindir}/xine-config
%{_mandir}/man1/xine-config.1.gz
%{_includedir}/xine.h
%dir %{_includedir}/xine
%{_includedir}/xine/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libxine.pc
%{_datadir}/aclocal/xine.m4
%dir %{_docdir}/xine-lib
%{_docdir}/xine-lib/*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.2.6-2
- Rebuild

