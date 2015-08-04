Name:           celt051
Version:        0.5.1.3
Release:        3
Summary:        An audio codec for use in low-delay speech and audio communication

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.celt-codec.org/
Source0:        http://downloads.us.xiph.org/releases/celt/celt-%{version}.tar.gz

BuildRequires: libogg-devel

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio
codec designed for realtime transmission of high quality speech and audio.
This is meant to close the gap between traditional speech codecs
(such as Speex) and traditional audio codecs (such as Vorbis).

The CELT bitstream format is not yet stable, this package is a special
version of 0.5.1 that has the same bitstream format, but symbols and files
renamed from 'celt*' to 'celt051*' so that it is parallel installable with
the normal celt for packages requiring this particular bitstream format.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: libogg-devel
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n celt-%{version}

%build
export CC=clang
export CXX=clang++

%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libcelt051.la

rpmclean
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/celtenc051
%{_bindir}/celtdec051
%{_libdir}/libcelt051.so.0
%{_libdir}/libcelt051.so.0.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/celt051
%{_libdir}/pkgconfig/celt051.pc
%{_libdir}/libcelt051.so

%changelog
