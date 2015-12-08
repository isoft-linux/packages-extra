Name: abi-tracker 
Version: 1.4
Release: 2
Summary: A tool to visualize ABI changes timeline of a C/C++ software library

License: GPL
URL: https://github.com/lvc/abi-tracker
Source0: %{name}.tar.gz

BuildRequires: perl
BuildRequires: gcc
BuildRequires: libstdc++
BuildRequires: libelfutils-devel

Requires: elfutils rfcdiff wget cmake automake gcc ctags binutils gawk wdiff

Provides: abi-compliance-checker >= 1.99.14
Provides: abi-dumper >= 0.99.12
Provides: abi-monitor >= 1.5
Provides: pkgdiff >= 1.7.0
Provides: vtable-dumper >= 1.1


%description
%{summary}

%prep
%setup -q -n %{name}

%build
%install
mkdir -p %{buildroot}/usr
for i in abi-compliance-checker abi-dumper abi-monitor pkgdiff vtable-dumper abi-tracker
do
   cd $i
   make install prefix=%{buildroot}/usr
   cd ..
done

%files
%{_bindir}/*
%{_datadir}/*

%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.4-2
- Initial build

