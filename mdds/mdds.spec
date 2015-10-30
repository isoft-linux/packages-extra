# header-only library
%global debug_package %{nil}

Name: mdds
Version: 0.12.1
Release: 7%{?dist}
Summary: A collection of multi-dimensional data structures and indexing algorithms

License: MIT
URL: https://gitlab.com/mdds/mdds
Source0: http://kohei.us/files/%{name}/src/%{name}_%{version}.tar.bz2

BuildRequires: boost-devel

%description
%{name} is a collection of multi-dimensional data structures and
indexing algorithms.

%package devel
Summary: Headers for %{name}
BuildArch: noarch
Requires: boost-devel
Provides: %{name}-static = %{version}-%{release}

%description devel
%{name} is a collection of multi-dimensional data structures and
indexing algorithms.
 
It implements the following data structures:
* segment tree
* flat segment tree 
* rectangle set
* point quad tree
* multi type matrix
* multi type vector

See README for a brief description of the structures.

%prep
%autosetup -n %{name}_%{version} -p1

%build
%configure

%install
install -d -m 0755 %{buildroot}/%{_includedir}/mdds
cp -pr include/mdds/* %{buildroot}/%{_includedir}/mdds
install -d -m 0755 %{buildroot}/%{_datadir}/pkgconfig
install -p -m 0644 misc/%{name}.pc %{buildroot}/%{_datadir}/pkgconfig

%check
make check %{?_smp_mflags}

%files devel
%{_includedir}/%{name}
%{_datadir}/pkgconfig/%{name}.pc
%doc AUTHORS NEWS README
%license COPYING

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.12.1-7
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.12.1-6
- Initial build 

