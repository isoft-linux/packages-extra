%global make_check 1

Summary: Library for accessing various audio file formats
Name: audiofile
Version: 0.3.6
Release: 10%{?dist}
Epoch: 1
# library is LGPL / the two programs GPL / see README
License: LGPLv2+ and GPLv2+
Source: http://audiofile.68k.org/%{name}-%{version}.tar.gz
URL: http://audiofile.68k.org/
BuildRequires: libtool
BuildRequires: alsa-lib-devel
BuildRequires: flac-devel

Patch0: audiofile-0.3.6-CVE-2015-7747.patch

%description
The Audio File library is an implementation of the Audio File Library
from SGI, which provides an API for accessing audio file formats like
AIFF/AIFF-C, WAVE, and NeXT/Sun .snd/.au files. This library is used
by the EsounD daemon.

Install audiofile if you are installing EsounD or you need an API for
any of the sound file formats it can handle.

%package devel
Summary: Development files for Audio File applications
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The audiofile-devel package contains libraries, include files, and
other resources you can use to develop Audio File applications.

%prep
%setup -q
%patch0 -p1 -b .CVE-2015-7747

%build
%configure --disable-static
make %{?_smp_mflags} LIBTOOL="/usr/bin/libtool"

%install
make DESTDIR="$RPM_BUILD_ROOT" install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a


%check
%if %{make_check}
make check
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING COPYING.GPL
%doc ACKNOWLEDGEMENTS AUTHORS NEWS NOTES README TODO
%{_bindir}/sfconvert
%{_bindir}/sfinfo
%{_libdir}/lib*.so.1*
%{_mandir}/man1/*

%files devel
%doc ChangeLog docs/*.3.txt
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1:0.3.6-10
- Initial build

