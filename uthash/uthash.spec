# This package builds a header-only lib, but has some testsuite to check
# the headers' function.  For this reason the main-pkg is build arched and
# produces a noarched subpkg, only.  There is no binary-compiled bits and
# therefore no debuginfo generated.
%global debug_package %{nil}

Name:           uthash
Version:        1.9.9
Release:        9%{?dist}
Summary:        A hash table for C structures
License:        BSD
URL:            http://troydhanson.github.io/uthash
Source0:        https://github.com/troydhanson/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%description
Any C structure can be stored in a hash table using uthash. Just add a
UT_hash_handle to the structure and choose one or more fields in your 
structure to act as the key. Then use these macros to store, retrieve or 
delete items from the hash table. 

%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
BuildArch:      noarch

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
# This is a header only package.

%install
install -d %{buildroot}%{_includedir}
install -pm0644 src/*.h %{buildroot}%{_includedir}/

%check
make %{?_smp_mflags} -C tests/

%files devel
%doc LICENSE doc/*.txt
%{_includedir}/ut*.h

%changelog
