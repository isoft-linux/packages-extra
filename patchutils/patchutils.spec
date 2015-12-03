Summary: A collection of programs for manipulating patch files
Name: patchutils
Version: 0.3.4
Release: 5%{?dist}
License: GPLv2+
URL: http://cyberelk.net/tim/patchutils/
Source0: http://cyberelk.net/tim/data/patchutils/stable/%{name}-%{version}.tar.xz
Patch1: patchutils-bz1226985.patch
Obsoletes: interdiff <= 0.0.10
Provides: interdiff = 0.0.11
BuildRequires: xmlto
BuildRequires: automake, autoconf

%description
This is a collection of programs that can manipulate patch files in
a variety of ways, such as interpolating between two pre-patches, 
combining two incremental patches, fixing line numbers in hand-edited 
patches, and simply listing the files modified by a patch.

%prep
%setup -q

# Fixed handling of delete-file diffs from git (bug #1226985).
%patch1 -p1 -b .bz1226985

autoreconf

%build
touch doc/patchutils.xml
%configure
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%{!?_licensedir:%global license %doc}
%doc AUTHORS ChangeLog README BUGS NEWS
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.3.4-5
- Init for isoft4

