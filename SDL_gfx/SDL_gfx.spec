Summary: SDL graphics drawing primitives and other support functions
Name: SDL_gfx
Version: 2.0.25
Release: 3
License: LGPLv2
Group: System Environment/Libraries
URL: http://www.ferzkopp.net/Software/SDL_gfx-2.0/
Source: http://www.ferzkopp.net/Software/SDL_gfx-2.0/SDL_gfx-%{version}.tar.gz
Patch0: SDL_gfx-2.0.13-ppc.patch
BuildRequires: SDL-devel
BuildRequires: libXt-devel

%description
Library providing SDL graphics drawing primitives and other support functions
wrapped up in an addon library for the Simple Direct Media (SDL) cross-platform
API layer.


%package devel
Summary: Development files for SDL_gfx
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: SDL-devel

%description devel
This package contains the files required to develop programs which use SDL_gfx.


%prep
%setup -q
%patch0 -p1 -b .ppc


%build
%configure \
%ifnarch %{ix86} x86_64
    --disable-mmx \
%endif
    --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/SDL/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
