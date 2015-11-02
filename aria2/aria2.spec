%define binname aria2c

Name:           aria2
Version:        1.19.2
Release:        3%{?dist}
Summary:        High speed download utility with resuming and segmented downloading
License:        GPLv2+ with exceptions
URL:            http://aria2.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         aria2-1.18.10-use-system-wide-crypto-policies.patch  
BuildRequires:  bison
BuildRequires:  c-ares-devel cppunit-devel
BuildRequires:  gettext gnutls-devel
BuildRequires:  libgcrypt-devel libxml2-devel
BuildRequires:  sqlite-devel
BuildRequires:  gettext

%description
aria2 is a download utility with resuming and segmented downloading.
Supported protocols are HTTP/HTTPS/FTP/BitTorrent. It also supports Metalink
version 3.0.

Currently it has following features:
- HTTP/HTTPS GET support
- HTTP Proxy support
- HTTP BASIC authentication support
- HTTP Proxy authentication support
- FTP support(active, passive mode)
- FTP through HTTP proxy(GET command or tunneling)
- Segmented download
- Cookie support
- It can run as a daemon process.
- BitTorrent protocol support with fast extension.
- Selective download in multi-file torrent
- Metalink version 3.0 support(HTTP/FTP/BitTorrent).
- Limiting download/upload speed

%prep
%setup -q
%patch0 -p1

%build
%configure --enable-bittorrent \
           --enable-metalink \
           --enable-epoll\
           --disable-rpath \
           --with-gnutls \
           --with-libcares \
           --with-libxml2 \
           --with-openssl \
           --with-libz \
           --with-sqlite3 \


V=1 make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING README 
%{_bindir}/%{binname}
%{_mandir}/man1/aria2c.1.gz
%{_mandir}/*/man1/aria2c.1.gz

%changelog
* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 1.19.2-3
- Initial build

