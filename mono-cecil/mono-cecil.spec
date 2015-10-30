Name:           mono-cecil
Version:        0.9.6
Release:        4
Summary:        Library to generate and inspect programs and libraries in the ECMA CIL form
License:        MIT
URL:            http://www.mono-project.com/Cecil
Source0:        https://github.com/jbevain/cecil/archive/%{version}/cecil-%{version}.tar.gz
Patch0:         %{name}-nobuild-tests.patch
BuildRequires:  mono
Requires:       mono

BuildArch: noarch

%global configuration net_4_5_Release

%description
Cecil is a library written by Jb Evain to generate and inspect programs and
libraries in the ECMA CIL format. It has full support for generics, and support
some debugging symbol format.

In simple English, with Cecil, you can load existing managed assemblies, browse
all the contained types, modify them on the fly and save back to the disk the
modified assembly.

Today it is used by the Mono Debugger, the bug-finding and compliance checking
tool Gendarme, MoMA, DB4O, as well as many other tools.

%prep
%setup -qn cecil-%{version}

# bundles nunit and we don't use them anyway
%patch0 -p1

%build
xbuild Mono.Cecil.sln /p:Configuration=%{configuration}

%install
mkdir -p %{buildroot}%{_libdir}/mono/gac
cd bin/%{configuration}/
gacutil -i Mono.Cecil.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Mdb.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Pdb.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Rocks.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
cd -

%files
%doc
%{_libdir}/mono/gac/Mono.Cecil*
%{_libdir}/mono/Mono.Cecil*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.9.6-4
- Rebuild

