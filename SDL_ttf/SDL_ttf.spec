Name:		SDL_ttf
Version:	2.0.11
Release:	7%{?dist}
Summary:	Simple DirectMedia Layer TrueType Font library

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL_ttf/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	zlib-devel


%description
This library allows you to use TrueType fonts to render text in SDL
applications.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/SDL/
%{_libdir}/pkgconfig/SDL_ttf.pc

%changelog
