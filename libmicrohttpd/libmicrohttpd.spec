Summary: Lightweight library for embedding a webserver in applications
Name: libmicrohttpd
Version: 0.9.46
Release: 3%{?dist}
License: LGPLv2+
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
URL: http://www.gnu.org/software/libmicrohttpd/
Source0: ftp://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
Patch0: gnutls-utilize-system-crypto-policy.patch

BuildRequires:  autoconf, automake, libtool
BuildRequires:	libcurl-devel
BuildRequires:  gnutls-devel
# for microspdy
BuildRequires:  openssl-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  graphviz
BuildRequires:  doxygen

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.
Key features that distinguish libmicrohttpd from other projects are:

* C library: fast and small
* API is simple, expressive and fully reentrant
* Implementation is http 1.1 compliant
* HTTP server can listen on multiple ports
* Support for IPv6
* Support for incremental processing of POST data
* Creates binary of only 25k (for now)
* Three different threading models

%package devel
Summary:        Development files for libmicrohttpd
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for libmicrohttpd

%package doc
Summary:        Documentation for libmicrohttpd
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Doxygen documentation for libmicrohttpd and some example source code

%package -n libmicrospdy
Summary:        Lightweight library for embedding a webserver using the SPDY protocol

%description -n libmicrospdy
GNU libmicrospdy is a small C library that is supposed to make it
easy to run a SPDY server as part of another application.

The library is part of the libmicrohttpd project and source tree
and shared its advantages of being fast aand small with a simple API.

%package -n libmicrospdy-devel
Summary:        Development files for libmicrospdy
Requires:       %{name} = %{version}-%{release}

%description -n libmicrospdy-devel
Development files for libmicrospdy

%package -n microspdy2http
Summary:        Translates incoming SPDY requests to http server on localhost

%description -n microspdy2http
Translates incoming SPDY requests to HTTP server on localhost.
* Uses libcurl
* No error handling for curl requests

%prep
%autosetup -p1

%build
# Required because patches modify .am files
autoreconf --install --force
%configure --disable-static --with-gnutls
make %{?_smp_mflags}
make -C doc/doxygen full

# Disabled for now due to problems reported at
# https://gnunet.org/bugs/view.php?id=1619
#check
#make check %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_bindir}/demo

# Install some examples in /usr/share/doc/libmicrohttpd-doc/examples
mkdir examples
install -m 644 src/examples/*.c examples

cp -R doc/doxygen/html html

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libmicrohttpd.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man3/libmicrohttpd.3.gz
%doc AUTHORS README ChangeLog
%doc examples
%doc html

%files -n libmicrospdy
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libmicrospdy.so.*

%files -n libmicrospdy-devel
%defattr(-,root,root,-)
%{_includedir}/microspdy.h
%{_libdir}/libmicrospdy.so
%{_libdir}/pkgconfig/libmicrospdy.pc

%files -n microspdy2http
%defattr(-,root,root,-)
%{_bindir}/microspdy2http

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 0.9.46-3
- Fix info issue, we never ship info

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 0.9.46-2
- Initial build

