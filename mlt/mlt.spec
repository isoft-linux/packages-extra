Name: mlt 
Version: 0.9.8
Release: 3
Summary: Media Lovin Toolkit

License: GPL 
URL: http://mltframework.org/bin/view/MLT
#https://github.com/mltframework/mlt/archive/v0.9.8.tar.gz
Source0: mlt-%{version}.tar.gz 

BuildRequires: frei0r-devel ffmpeg-devel 
BuildRequires: SDL-devel sox-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: libX11-devel
BuildRequires: alsa-lib-devel
BuildRequires: libexif-devel
BuildRequires: fftw3-devel
BuildRequires: libsamplerate-devel
BuildRequires: libxml2-devel

BuildRequires: swig

Requires: frei0r-plugins

%description
An open source multimedia framework, designed and developed for television broadcasting. 
It provides a toolkit for broadcasters, video editors, media players, transcoders, web streamers and many more types of applications.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
    --avformat-vdpau         \
    --enable-gpl             \
    --enable-gpl3            \
    --enable-opengl          \
    --disable-gtk2           \
    --qt-libdir=%{_libdir}  \
    --qt-includedir=%{_libdir}/qt5/include

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/melt
%{_libdir}/libmlt*.so.*
%{_libdir}/mlt/libmlt*.so
%{_datadir}/mlt

%files devel
%{_libdir}/libmlt*.so
%{_includedir}/mlt++ 
%{_includedir}/mlt
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.9.8-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.9.8-2
- Initial build 


