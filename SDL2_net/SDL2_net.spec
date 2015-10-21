Name:		SDL2_net
Version:    2.0.0
Release:	1
Summary:	Network library for SDL2

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL2_net/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz

BuildRequires: 	SDL2-devel >= 1.2.10

%description
Simple DirectMedia Layer (SDL2) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.  This is an example portable network library for use with SDL.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL2-devel >= 1.2.10
Requires:	pkgconfig


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure \
	--disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install /usr/bin/install showinterfaces $RPM_BUILD_ROOT%{_bindir}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/showinterfaces
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/SDL2/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

