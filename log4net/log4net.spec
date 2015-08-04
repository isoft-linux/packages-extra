%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac

Name:	 	log4net
URL:		http://logging.apache.org/log4net/
License:	ASL 2.0
Group:		System Environment/Libraries
Version:	1.2.13
Release:	5%{?dist}
Summary:	A .NET framework for logging
Source:		http://mirror.reverse.net/pub/apache/logging/log4net/source/%{name}-%{version}-src.zip

BuildRequires:	mono
BuildRequires:	mono-devel
BuildRequires:	nant


# %define debug_package %{nil}
# This is a mono package

%description
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%package devel
Summary:	A .NET framework for logging
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%prep
%setup -q
sed -i 's/\r//' NOTICE
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE
# Remove prebuilt dll files
rm -rf bin/

mv src/Layout/XMLLayout.cs src/Layout/XmlLayout.cs
mv src/Layout/XMLLayoutBase.cs src/Layout/XmlLayoutBase.cs

# Fix for mono 4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

# Use system mono.snk key
sed -i -e 's!"..\\..\\..\\log4net.snk")]!"/etc/pki/mono/mono.snk")]!' src/AssemblyInfo.cs
sed -i -e 's!|| SSCLI)!|| SSCLI || MONO)!' src/AssemblyInfo.cs


%build
# ASF recommend using nant to build log4net
xbuild /property:Configuration=Debug /property:DefineConstants=DEBUG,MONO,STRONG src/log4net.vs2010.csproj
#nant -buildfile:log4net.build compile-all

%install
# install pkgconfig file
cat > %{name}.pc <<EOF
Name: log4net
Description: log4net - .Net logging framework
Version: %{version}
Libs: -r:%{_monodir}/log4net/log4net.dll
EOF

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
cp %{name}.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT/%{_monogacdir}

#gacutil -i bin/mono/2.0/release/log4net.dll -f -package log4net -root ${RPM_BUILD_ROOT}/%{_prefix}/lib
gacutil -i build/bin/net/2.0/debug/log4net.dll -f -package log4net -root ${RPM_BUILD_ROOT}/%{_prefix}/lib

%files
%{_monogacdir}/log4net
%{_monodir}/log4net
%doc LICENSE NOTICE README.txt

%files devel
%{_libdir}/pkgconfig/log4net.pc

%changelog
