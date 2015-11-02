Name:           leveldb
Version:        1.18
Release:        1%{?dist}
Summary:        A fast and lightweight key/value database library by Google
License:        BSD
URL: https://github.com/google/leveldb
Source0: %{name}-%{version}.tar.gz
#pkgconfig file
Source1: leveldb.pc.in

BuildRequires:  snappy-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        The development files for %{name}
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Additional header files for development with %{name}.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_docdir}/%{name}

#libraries
install -m 0755 libleveldb.so.%{version} %{buildroot}%{_libdir}
install -m 0644 libleveldb.a %{buildroot}%{_libdir}
cp -P libleveldb.so.1 libleveldb.so %{buildroot}%{_libdir}

#headers
install -m 0644 include/leveldb/* %{buildroot}%{_includedir}/%{name}

#pkgconfig file
install -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
sed -i 's|@prefix@|%{_prefix}|g' %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
sed -i 's|@exec_prefix@|%{_exec_prefix}|g' %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
sed -i 's|@libdir@|%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
sed -i 's|@includedir@|%{_includedir}|g' %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
sed -i 's|@PACKAGE_VERSION@|%{version}|g' %{buildroot}%{_libdir}/pkgconfig/leveldb.pc

#docs
cp -r doc/* %{buildroot}%{_docdir}/%{name}/

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/lib%{name}.so.*

%files devel
%{_pkgdocdir}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 1.18-1
- Initial build

