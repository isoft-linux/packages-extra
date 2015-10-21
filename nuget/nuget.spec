Name:           nuget
Version:        2.8.3
Release:        3.21
Summary:        DotNet package manager
Group:          Development/Languages/Mono
License:        Apache-2.0
URL:            https://nuget.codeplex.com/
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.sh
Source3:        xdt.tar.gz
# Prevent build process from fetching external packages
Source4:        packages.tgz

#helper scripts to import certs of some sites.
Source10:       nuget-import-certs

BuildArch:      noarch
BuildRequires:  dos2unix
BuildRequires:  mono-devel
# The post install will fail on OBS due to missing network connectivity.

Requires:       mono

%description
NuGet is the package manager for the Microsoft development platform including .NET.
The NuGet client tools provide the ability to produce and consume packages.
The NuGet Gallery (nuget.org) is the central package repository used by all package
authors and consumers.

%package devel
Summary:        Development files for NuGet
Group:          Development/Languages/Mono
Requires:       nuget = %{version}

%description devel
This package contains development files for NuGet integration.

%prep
%setup -q -n %{name}-%{version} -a 3 -a 4
#fix build with pure mono .net 4.5
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;

find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

find . -name "*.proj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;


dos2unix LICENSE.txt
dos2unix COPYRIGHT.txt
dos2unix CREDITS.txt

%build
xbuild /p:Configuration=Release xdt/XmlTransform/Microsoft.Web.XmlTransform.csproj
cp xdt/XmlTransform/obj/Release/Microsoft.Web.XmlTransform.dll* lib/
xbuild Build/Build.proj /p:Configuration=Release /p:TreatWarningsAsErrors=false /tv:4.0 /p:TargetFrameworkVersion=v4.5 /p:Configuration="Mono Release" /t:GoMono

%install
install -d %{buildroot}%{_prefix}/lib/nuget
install -m 0644 src/CommandLine/obj/Mono\ Release/NuGet.exe %{buildroot}%{_prefix}/lib/nuget/
install -m 0644 src/Core/obj/Mono\ Release/NuGet.Core.dll %{buildroot}%{_prefix}/lib/nuget/
install -m 0644 lib/Microsoft.Web.XmlTransform.dll %{buildroot}%{_prefix}/lib/nuget/

install -d %{buildroot}%{_bindir}
install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/nuget

install -m 0755 %{SOURCE10} %{buildroot}%{_bindir}/nuget-import-certs

mkdir -p %{buildroot}%{_datadir}/pkgconfig
cat <<EOF > %{buildroot}%{_datadir}/pkgconfig/nuget-core.pc
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include
Libraries=\${prefix}/lib/nuget/NuGet.Core.dll \${prefix}/lib/nuget/Microsoft.Web.XmlTransform.dll

Name: nuget-core
Description: Library for acessing Microsoft NuGet repositories
Version: %{version}
Libs: -r:\${libdir}/nuget/NuGet.Core.dll -r:\${libdir}/nuget/Microsoft.Web.XmlTransform.dll
EOF

%post
#mozroots --import --machine --sync
#certmgr -ssl -m https://go.microsoft.com
#certmgr -ssl -m https://nugetgallery.blob.core.windows.net
#certmgr -ssl -m https://nuget.org

%files
%defattr(-, root, root)
%{_bindir}/*
%{_prefix}/lib/nuget
%doc *.txt

%files devel
%defattr(-, root, root)
%{_datadir}/pkgconfig/nuget-core.pc

%changelog
