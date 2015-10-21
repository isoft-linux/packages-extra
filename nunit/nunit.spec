Name:           nunit
Version:        2.6.4
Release:        1.7
License:        Zlib
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Url:            http://www.nunit.org/
Source:         https://github.com/nunit/nunitv2/archive/%{version}.tar.gz
BuildRequires:  mono-devel dos2unix strace libgdiplus fdupes
Group:          Development/Libraries/Mono
Summary:        Unit-testing framework for all .NET languages

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

%package devel
Summary:        Development files for NUnit
Group:          Development/Languages/Mono
Requires:       nunit = %{version}

%description devel
This package contains development files for NUnit integration.


# require older mono runtime
%filter_requires_in %{_prefix}/lib/nunit/
# Also filter provides of the prebuilt DLLs
%filter_provides_in %{_prefix}/lib/nunit/
%filter_setup


%prep
%setup -q -n nunitv2-%{version}

# Remove prebuilt binaries
#find . -name "*.dll" -not -path "./mcs/class/lib/monolite/*" -print -delete
#find . -name "*.exe" -not -path "./mcs/class/lib/monolite/*" -print -delete

#use mono .net 4.5 framework
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;


%build
xbuild nunit.sln /t:Rebuild /p:Configuration=Debug

%install
mkdir -p "%{buildroot}%{_prefix}/lib/nunit"
cp -a bin/Debug/* "%{buildroot}%{_prefix}/lib/nunit"
mkdir -p "%{buildroot}%{_docdir}/%{name}"
cp -a license.txt "%{buildroot}%{_docdir}/%{name}/"
cp -a doc "%{buildroot}%{_docdir}/%{name}/"
cp -a samples "%{buildroot}%{_docdir}/%{name}/"

mkdir -p "%{buildroot}%{_bindir}"
echo '#!/bin/sh
exec /usr/bin/mono %{_prefix}/lib/nunit/nunit.exe "$@"' > "%{buildroot}%{_bindir}/nunit"
chmod +x "%{buildroot}%{_bindir}/nunit"

cd %{buildroot}%{_docdir}/%{name}/
find . -type f -exec dos2unix {} \;

for i in nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.util.dll lib/nunit-console-runner.dll lib/nunit-gui-runner.dll lib/nunit.uiexception.dll lib/nunit.uikit.dll framework/nunit.mocks.dll ; do
	gacutil -i %{buildroot}%{_prefix}/lib/nunit/$i -package nunit -root %{buildroot}%{_prefix}/lib
	rm -f %{buildroot}%{_prefix}/lib/nunit/$i
done

mkdir -p %{buildroot}%{_datadir}/pkgconfig
cat <<EOF > %{buildroot}%{_datadir}/pkgconfig/nunit.pc
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
pkglibdir=\${prefix}/lib/mono/nunit

Name: NUnit
Description: Testing framework for .NET
Version: %{version}
Libs: -r:\${pkglibdir}/nunit.core.dll -r:\${pkglibdir}/nunit.core.interfaces.dll -r:\${pkglibdir}/nunit.framework.dll -r:\${pkglibdir}/nunit.util.dll r:\${pkglibdir}/nunit-console-runner.dll r:\${pkglibdir}/nunit-gui-runner.dll r:\${pkglibdir}/nunit.uiexception.dll r:\${pkglibdir}/nunit.uikit.dll r:\${pkglibdir}/nunit.mocks.dll
EOF

%fdupes %{buildroot}%{_prefix}

#rm -rf %{buildroot}/%{_libdir}/nunit/log4net.dll

%files
%defattr(-,root,root)
%{_prefix}/lib/nunit
%{_prefix}/lib/mono/nunit
%{_prefix}/lib/mono/gac/nunit*
%{_bindir}/nunit
%{_docdir}/nunit

%files devel
%defattr(-, root, root)
%{_datadir}/pkgconfig/nunit.pc
%changelog
