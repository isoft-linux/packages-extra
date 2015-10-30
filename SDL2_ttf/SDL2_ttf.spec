Name:		SDL2_ttf
Version:    2.0.12
Release:	2
Summary:	Truetype font library for SDL2

License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL2_ttf/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
Patch0: SDL2_ttf-disable-glfont.patch

BuildRequires: 	SDL2-devel >= 1.2.10

%description
Simple DirectMedia Layer (SDL2) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This library is a wrapper around the excellent FreeType 2.0 library.


%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	SDL2-devel >= 1.2.10
Requires:	pkgconfig


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
touch NEWS README AUTHORS ChangeLog
autoreconf -ivf
%configure \
	--disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install /usr/bin/install showfont $RPM_BUILD_ROOT%{_bindir}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/showfont
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/SDL2/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0.12-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

