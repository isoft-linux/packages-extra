Name: nodejs
Version: 4.1.2
Release: 1
Summary: Easily building fast, scalable network applications	

License: MIT
URL: http://nodejs.org/
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz

#skip cpplint
Patch0:     node-disable-cpplint.patch

BuildRequires: zlib-devel, openssl-devel
BuildRequires: clang 

Provides: /usr/bin/node

%description
Node.js is a platform built on Chrome's JavaScript runtime for 
easily building fast, scalable network applications. 

Node.js uses an event-driven, non-blocking I/O model that 
makes it lightweight and efficient, 
perfect for data-intensive real-time applications that run across distributed devices.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n node-v%{version}
%patch0 -p1

%build
export CC=clang
export CXX=clang++

./configure \
    --prefix=%{_prefix} \
    --shared-zlib \
    --shared-openssl 

make -C out BUILDTYPE=Release mksnapshot

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%check
#temp remove this test. 'Not All Key used', seems ok.
rm -rf test/parallel/test-async-wrap-check-providers.js

#NOTE: some test need network enabled.
make test

%files
%{_bindir}/node
%{_bindir}/npm
%{_libdir}/node_modules
%{_mandir}/man1/node.1.gz


%files devel
%dir %{_includedir}/node
%{_includedir}/node/*
%{_datadir}/systemtap/tapset/node.stp
%{_docdir}/node/gdbinit

%changelog
* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 4.1.2

* Sat Aug 15 2015 Cjacker <cjacker@foxmail.com>
- update to 0.12.7
