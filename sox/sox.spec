Summary: A general purpose sound file conversion tool
Name: sox
Version: 14.4.2
Release: 5%{?dist}
License: GPLv2+ and LGPLv2+ and MIT
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
URL: http://sox.sourceforge.net/
BuildRequires: libvorbis-devel
BuildRequires: alsa-lib-devel, libtool-ltdl-devel, libsamplerate-devel
BuildRequires: gsm-devel, wavpack-devel, libpng-devel
BuildRequires: flac-devel, libao-devel, libsndfile-devel, libid3tag-devel
BuildRequires: pulseaudio-libs-devel, opusfile-devel
BuildRequires: libtool

%description
SoX (Sound eXchange) is a sound file format converter SoX can convert
between many different digitized sound formats and perform simple
sound manipulation functions, including sound effects.

%package -n  sox-devel
Summary: The SoX sound file format converter libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description -n sox-devel
This package contains the library needed for compiling applications
which will use the SoX sound file format converter.

%prep
%setup -q
#regenerate scripts from older autoconf to support aarch64
autoreconf -vfi

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" 
%configure \
    --with-lpc10 \
    --with-gsm \
    --includedir=%{_includedir}/sox \
    --disable-static \
    --with-distro=iSoft \
    --with-alsa=dyn \
    --with-ao=dyn \
    --with-caf=dyn \
    --with-fap=dyn \
    --with-mat4=dyn \
    --with-mat5=dyn \
    --with-opus=dyn \
    --with-paf=dyn \
    --with-pulseaudio=dyn \
    --with-pvf=dyn \
    --with-sd2=dyn \
    --with-sndfile=dyn \
    --with-vorbis=dyn \
    --with-w64=dyn \
    --with-wavpack=dyn \
    --with-xi=dyn
#--with-dyn-default is broken (flac and oss dont link), therefore plugins enumerated explicitly
#--with-flac=dyn \
#--with-oss=dyn \

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libsox.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sox/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sox/*.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox
%{_bindir}/soxi
%{_libdir}/libsox.so.*
%dir %{_libdir}/sox/
%{_libdir}/sox/libsox_fmt_*.so
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n sox-devel
%{_includedir}/sox
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_mandir}/man3/*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 14.4.2-5
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 14.4.2-4
- Initial build

