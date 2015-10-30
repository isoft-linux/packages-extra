Summary: SDL2 graphics drawing primitives and other support functions
Name: SDL2_gfx
Version: 1.0.0
Release: 8%{?dist}
License: zlib
URL: http://www.ferzkopp.net/Software/SDL2_gfx-2.0/
Source: http://downloads.sourceforge.net/project/sdl2gfx/%{name}-%{version}.tar.gz
Patch0: 0001-test-Add-batch-switch.patch
BuildRequires: SDL2-devel
BuildRequires: doxygen

%description
Library providing graphics drawing primitives and other support functions
wrapped up in an addon library for the Simple Direct Media version 2 (SDL2)
cross-platform API layer.


%package devel
Summary: Development files for SDL2_gfx
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: SDL2-devel%{?_isa}

%description devel
This package contains the files required to develop programs which use SDL2_gfx.



%prep
%setup -q
%patch0 -p1
find -name '*.[ch]' |xargs chmod -x
sed 's/\r//' <README >README.unix
touch -r README README.unix
mv README.unix README


%build
%configure \
%ifnarch %{ix86} x86_64
    --disable-mmx \
%endif
    --disable-static
make %{?_smp_mflags}

# Examples & test suite
cd test
CFLAGS='-I.. -L../.libs %{optflags}'
%configure
make %{_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Missing from Makefile.am
install -pm644 SDL2_gfxPrimitives_font.h %{buildroot}%{_includedir}/SDL2/

# This might be useful for live tests; ship it in the devel package
install -d %{buildroot}%{_libdir}/%{name}
install test/testgfx %{buildroot}%{_libdir}/%{name}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
export SDL_VIDEODRIVER=dummy
export LD_LIBRARY_PATH="$PWD/.libs"
cd test
./testgfx --info all --log all --batch
./testrotozoom --info all --log all --batch
./testimagefilter


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/SDL2/*.h
%{_libdir}/*.so
%{_libdir}/%{name}


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.0.0-8
- Rebuild

