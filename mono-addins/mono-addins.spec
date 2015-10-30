%define name mono-addins
%define version 1.1 
%define release 2

Summary: generic framework for creating extensible applications 
Name:    mono-addins 
Version: 1.1
Release: 1
URL:     http://www.mono-project.com
Source0: http://download.mono-project.com/sources/mono-addins/%{name}-%{version}.tar.gz
Patch0:  mono-addins-1.0-libdir.patch
License: BSD
BuildRequires: mono >= 3.0 
BuildRequires: gtk2-sharp-gapi

BuildArch: noarch
%description
Mono.Addins is a generic framework for creating extensible applications,
and for creating libraries which extend those applications.

%prep
%setup -q
%build
sed -i "s#AC_PATH_PROG(MCS, gmcs, no)#AC_PATH_PROG(MCS, mcs, no)#g" configure.ac
autoreconf -vif
%configure --enable-gui
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/mautil
%{_libdir}/mono/gac/*
%{_libdir}/mono/mono-addins
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/mautil.1.gz

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.1-1
- Rebuild

