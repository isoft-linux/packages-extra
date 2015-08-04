Summary: Tree is a recursive directory listing command
Name: tree
Version: 1.6.0
Release: 1 
License: LGPLv2+
Group: Core/Runtime/Utility
Source0: %{name}-%{version}.tgz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
Tree is a recursive directory listing command that produces a depth indented listing of files
%prep
%setup
%build
make 
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
make install prefix=$RPM_BUILD_ROOT/%{_prefix} MANDIR=$RPM_BUILD_ROOT/%{_prefix}/share/man/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
%{_bindir}/tree
%{_mandir}/man1/*
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

