Name:		SDL_image
Version:	1.2.12
Release:	3
Summary:	Image loading library for SDL

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL_image/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz

BuildRequires: 	SDL-devel >= 1.2.10
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This package contains a simple library for loading images of
various formats (BMP, PPM, PCX, GIF, JPEG, PNG) as SDL surfaces.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.10
Requires:	pkgconfig


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-dependency-tracking	\
	--enable-tif				\
	--disable-jpg-shared			\
	--disable-png-shared			\
	--disable-tif-shared			\
	--disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install /usr/bin/install showimage $RPM_BUILD_ROOT%{_bindir}/showimage-1

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_bindir}/showimage-1
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/SDL/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- rename showimage to showimage-1 to avoid conflicts with SDL2_image
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

