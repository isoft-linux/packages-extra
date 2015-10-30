Summary: A cross-platform multimedia library
Name: SDL2
Version: 2.0.3
Release: 9
URL: http://www.libsdl.org/
License: LGPLv2+

Source0: %{name}-%{version}.tar.gz
Source1: SDL2-backend.sh


#BuildRequires: audiofile-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: automake autoconf libtool
%ifarch %{ix86}
BuildRequires: nasm
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.

%package devel
Summary: Files needed to develop Simple DirectMedia Layer applications
Requires: SDL2 = %{version}-%{release} alsa-lib-devel
Requires: pkgconfig
Requires: automake

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the libraries, include files, and other
resources needed for developing SDL applications.

%package static
Summary: Files needed to develop static Simple DirectMedia Layer applications
Requires: SDL2-devel = %{version}-%{release}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the static libraries needed for developing
static SDL applications.

%prep
%setup -q -b0

%build
%configure \
   --enable-sdl-dlopen \
   --enable-pulseaudio \
   --enable-pulseaudio-shared \
   --enable-alsa \
   --enable-video-wayland \
   --enable-wayland-shared \
   --enable-video-opengles \
   --enable-video-opengl \
   --enable-video-x11 \
   --enable-x11-shared \
   --enable-dbus \
   --enable-libudev \
   --disable-rpath
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/SDL2-backend.sh
%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/SDL2-backend.sh
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl*.pc
%{_includedir}/SDL*
%{_datadir}/aclocal/*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0.3-9
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

