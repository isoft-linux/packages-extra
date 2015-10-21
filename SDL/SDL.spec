Summary: A cross-platform multimedia library
Name: SDL
Version: 1.2.15
Release: 8
Source0: %{name}-%{version}.tar.gz
Patch0: SDL-1.2.10-GrabNotViewable.patch  
Patch1: SDL-1.2.15-const_XData32.patch
Patch7: SDL-remove-esd.patch

URL: http://www.libsdl.org/
License: LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libXext-devel libX11-devel
BuildRequires: libGL-devel libGLU-devel
BuildRequires: libXrender-devel libXrandr-devel gettext-devel
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
Group: Development/Libraries
Requires: SDL = %{version}-%{release} alsa-lib-devel
Requires: libX11-devel
Requires: libXext-devel
Requires: libGL-devel
Requires: libGLU-devel
Requires: libXrender-devel
Requires: libXrandr-devel
Requires: pkgconfig
Requires: automake

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the libraries, include files, and other
resources needed for developing SDL applications.

%package static
Summary: Files needed to develop static Simple DirectMedia Layer applications
Group: Development/Libraries
Requires: SDL-devel = %{version}-%{release}

%description static
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device. This package provides the static libraries needed for developing
static SDL applications.

%prep
%setup -q -b0
%patch0 -p1
%patch1 -p1
%patch7 -p1

%build
aclocal
libtoolize
autoconf
%configure \
   --disable-video-svga --disable-video-ggi --disable-video-aalib \
   --enable-sdl-dlopen \
   --enable-arts-shared \
   --enable-esd-shared \
   --enable-pulseaudio-shared \
   --enable-alsa \
   --disable-video-ps3 \
   --disable-rpath

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la

rpmclean
%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl.pc
%{_includedir}/SDL
%{_datadir}/aclocal/*
%{_mandir}/man3/SDL*.3*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

