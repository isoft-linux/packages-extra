Name:		xsp
Version:	3.8
Release:	2%{?dist}
License:	MIT
URL:		http://www.mono-project.com/Main_Page
Summary:	A small web server that hosts ASP.NET
Group:		System Environment/Daemons

Source0:	http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	mono-devel
#for monodoc
BuildRequires:	mono-tools
BuildRequires:	autoconf automake libtool
Requires:	mono

%define debug_package %{nil}

%description

XSP is a standalone web server written in C# that can be used to run ASP.NET 
applications as well as a set of pages, controls and web services that you can 
use to experience ASP.NET.
	  
%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} pkgconfig
Summary: Development files for xsp

%description devel
Development files for xsp

%package tests
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Summary: xsp test files

%description tests
Files for testing the xsp server

%prep
%setup -q

sed -i "s#gmcs#mcs#g" configure
sed -i "s#mono/2.0#mono/4.5#g" configure
sed -i "s#Mono 2.0#Mono 4.5#g" configure
sed -i "s#mono/4.0#mono/4.5#g" configure
sed -i "s#Mono 4.0#Mono 4.5#g" configure

%build
%configure --libdir=%{_prefix}/lib
make

%install
make DESTDIR=%{buildroot} install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

%files
%doc NEWS README COPYING
%{_bindir}/asp*
%{_bindir}/dbsessmgr*
%{_bindir}/mod-mono*
%{_bindir}/mono-fpm
%{_bindir}/shim
%{_bindir}/xsp*
%{_bindir}/fastcgi-mono-server*
%{_prefix}/lib/xsp
%{_prefix}/lib/mono/gac/Mono.WebServer*/
%{_prefix}/lib/mono/gac/fastcgi-mono-server2
%{_prefix}/lib/mono/gac/fastcgi-mono-server4
%{_prefix}/lib/mono/gac/mod-mono-server*/
%{_prefix}/lib/mono/gac/mono-fpm
%{_prefix}/lib/mono/gac/xsp*/
%{_prefix}/lib/mono/2.0/*.dll
%{_prefix}/lib/mono/2.0/*.exe
%{_prefix}/lib/monodoc/sources/Mono.WebServer.*
%{_prefix}/lib/monodoc/sources/Mono.FastCGI.*
%{_prefix}/lib/mono/4.?/Mono.WebServer2.dll
%{_prefix}/lib/mono/4.?/fastcgi-mono-server4.exe
%{_prefix}/lib/mono/4.?/mod-mono-server4.exe
%{_prefix}/lib/mono/4.?/mono-fpm.exe
%{_prefix}/lib/mono/4.?/xsp4.exe
%{_prefix}/lib/libfpm_helper.so.0*
%{_mandir}/man1/asp*
%{_mandir}/man1/dbsessmgr*
%{_mandir}/man1/mod-mono-server*
%{_mandir}/man1/xsp*
%{_mandir}/man1/fastcgi-mono-server*

%files devel
%{_libdir}/pkgconfig/xsp*
%{_prefix}/lib/libfpm_helper.so

%files tests
%{_prefix}/lib/xsp/2.0
%{_prefix}/lib/xsp/test

%changelog
