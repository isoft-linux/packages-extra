%define name mono-basic
%define version 4.0.1
%define release 3 

Summary: Visual Basic .NET support for Mono
Name:    mono-basic 
Version: 4.0.1
Release: 1
Source0: http://download.mono-project.com/sources/mono-basic/%{name}-%{version}.tar.bz2
License: BSD
URL:		http://www.go-mono.com/ 
BuildRequires: mono-devel >= 1.2.4
BuildArch: noarch

%description
This package contains the Visual Basic .NET compiler and language
runtime. This allows you to compile and run VB.NET application and
assemblies.

%prep
%setup -q -n %name-%version

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
cp -r $RPM_BUILD_ROOT/usr/bin/vbnc $RPM_BUILD_ROOT/usr/bin/mbas
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_bindir/vbnc*
%_bindir/mbas
%{_libdir}/mono/*
%{_mandir}/man1/*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.0.1-1
- Rebuild

