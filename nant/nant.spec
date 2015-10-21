%global debug_package %{nil}
%global monodir %{_prefix}/lib
%global bootstrap 1

Summary: NAnt is a build tool for Mono and .NET
Name: nant
Version: 0.92
Release: 1%{?dist}
Epoch: 1
License: GPLv2+
Group: Development/Tools
Url: http://nant.sourceforge.net/

Source0: http://downloads.sourceforge.net/nant/%{name}-%{version}-src.tar.gz
Patch1: nant-0.92-no_ndoc.patch
Patch2: nant-0.92-system_nunit.patch
Patch3: nant-0.90-no_sharpcvslib.patch
Patch4: nant-0.90-system_sharpziplib.patch
Patch5: nant-0.92-system_log4net.patch

BuildRequires: mono-devel

%if 0%{bootstrap}
# Nothing here if we're bootstrapping
%else
BuildRequires: log4net-devel
%endif

%if 0%{bootstrap}
# In bootstrap mode, filter requires of the prebuilt DLLs. Some of these
# require older mono runtime, creating broken rpm deps.
%filter_requires_in %{_prefix}/lib/NAnt/
# Also filter provides of the prebuilt DLLs
%filter_provides_in %{_prefix}/lib/NAnt/
%filter_setup
%endif

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%package docs
Summary:	Documentation package for nant
Group:	Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description docs
Documentation for nant

%package devel
Summary:	Development file for nant
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development file for %{name}

%prep
%setup -q -n %{name}-%{version}

# install to libdir instead of datadir
sed -i -e "/property name=\"install\.share\"/ s/'share'/'lib'/" NAnt.build
sed -i -e "s,/share/,/lib/," etc/nant.pc.in

%if 0%{bootstrap}
# do nothing
%else

# Remove NDoc support
%patch1 -p1 -b .no_ndoc
rm src/NAnt.DotNet/Tasks/NDocTask.cs
find lib -name 'NDoc*.dll' | xargs rm

# Remove NUnit1 support and fix build with system NUnit.
# Based on Debian's 004-nant-nunit_2.4.dpatch
%patch2 -p1 -b .system_nunit
find lib -iname 'nunit*' | xargs rm
%endif

# Remove SharpCvsLib support
%patch3 -p1 -b .no_sharpcvslib
find lib -name "*SharpCvsLib*.dll" | xargs rm
find lib -name "scvs.exe" | xargs rm

# Use system SharpZipLib which is older than the one bundled with nant
# https://bugzilla.novell.com/show_bug.cgi?id=426065
%patch4 -p1 -F 3 -b .system_sharpziplib
find lib -name "*SharpZipLib*.dll" | xargs rm

find . -type d|xargs chmod 755
find . -type f|xargs chmod 644
sed -i 's/\r//' doc/license.html
sed -i 's/\r//' COPYING.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' doc/releasenotes.html

# Clean out the prebuilt files (unless we're bootstrapping)
# If we're not bootstrapping, leave the files alone:
%if 0%{bootstrap}
echo "BOOTSTRAP BUILD"
%else
echo "NORMAL BUILD, NUKING PREBUILT BUNDLED DLL FILES"
rm -rf lib/*
%endif

# Use system log4net, unless we're bootstrapping.
%if 0%{bootstrap}
# do nothing
%else
%patch5 -p1 -b .system_log4net
%endif

#Fixes for Mono 4
sed -i "s#gmcs#mcs#g" Makefile
sed -i "s#TARGET=mono-2.0#TARGET=mono-4.0#g" Makefile
sed -i "s#mono/4.0#mono/4.5#g" src/NAnt.Console/App.config
sed -i "s#dmcs#mcs#g" src/NAnt.Console/App.config
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
make

%install
rm -rf %{buildroot}
make install prefix=%{_prefix} DESTDIR=%{buildroot}
find examples -name \*.dll -o -name \*.exe|xargs rm -f
rm -rf %{buildroot}%{_datadir}/NAnt/doc
rm -rf %{buildroot}%{_prefix}/lib/doc/NAnt

# Flush out the binary bits that we used to build, unless we're bootstrapping.
%if 0%{bootstrap}
# Do nothing
%else
rm -rf %{buildroot}%{_prefix}/lib/NAnt/bin/lib
rm -rf %{buildroot}%{_prefix}/lib/NAnt/bin/log4net.dll
%endif

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING.txt
%doc README.txt doc/*.html
%{_bindir}/nant
%{monodir}/NAnt/

%files docs
%doc examples/* doc/help/*

%files devel
%{_libdir}/pkgconfig/nant.pc

%changelog
