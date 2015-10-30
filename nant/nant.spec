%global debug_package %{nil}
%global monodir %{_prefix}/lib

%global bootstrap 0 

Summary: NAnt is a build tool for Mono and .NET
Name: nant
Version: 0.93
Release: 5.git%{?dist}
Epoch: 1
License: GPLv2+
Url: http://nant.sourceforge.net/

#http://nant.sourceforge.net/nightly/latestA
Source0: nant-master.zip

Patch1: nant-0.92-no_ndoc.patch
Patch2: nant-0.92-system_nunit.patch
Patch3: nant-0.90-no_sharpcvslib.patch
Patch4: nant-0.90-system_sharpziplib.patch
Patch5: nant-0.92-system_log4net.patch
Patch6: nant-0.92-no_netdumbster.patch
Patch7: nant-build-fix.patch

BuildRequires: mono-devel
BuildRequires: nunit-devel >= 2.6.4

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
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description docs
Documentation for nant

%package devel
Summary:	Development file for nant
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development file for %{name}

%prep
%setup -q -n %{name}-master

# install to libdir instead of datadir
sed -i -e "/property name=\"install\.share\"/ s/'share'/'lib'/" NAnt.build
sed -i -e "s,/share/,/lib/," etc/nant.pc.in

# Remove NDoc support
%patch1 -p1 -b .no_ndoc
rm src/NAnt.DotNet/Tasks/NDocTask.cs
rm -Rf src/NDoc.Documenter.NAnt
find lib -name 'NDoc*.dll' | xargs rm

# Remove NUnit1 support and fix build with system NUnit.
# Based on Debian's 004-nant-nunit_2.4.dpatch
%patch2 -p1 -b .system_nunit
find lib -iname 'nunit*' | xargs rm

# Remove SharpCvsLib support
%patch3 -p1 -b .no_sharpcvslib
find lib -name "*SharpCvsLib*.dll" | xargs rm
find lib -name "scvs.exe" | xargs rm

# Use system SharpZipLib which is older than the one bundled with nant
# https://bugzilla.novell.com/show_bug.cgi?id=426065
%patch4 -p1 -F 3 -b .system_sharpziplib
find lib -name "*SharpZipLib*.dll" | xargs rm

%patch6 -p1 -b .no_netdumbster
rm tests/NAnt.Core/Tasks/MailTaskTest.cs

#remove this file.
rm -rf ./etc/"Reference Resolution in Visual Studio.htm"

find . -type d |xargs chmod 755
find . -type f |xargs chmod 644

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

%patch7 -p1

%build
make TARGET=mono-4.0 MCS="mcs -sdk:4"

%install
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
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 1:0.93-5
- Rebuild

