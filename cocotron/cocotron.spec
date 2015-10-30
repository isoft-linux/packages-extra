Name: cocotron
Version: 20150727
Release: 2
Summary: A cross platform implementation of the Apple Foundation API.	
URL: http://www.cocotron.org
License: MIT
#git clone https://github.com/cjwl/cocotron.git
Source0: cocotron.tar.gz

Patch1: 001-fix-build-cflags-defines.patch
Patch2: 002-fix-nsstring-encoding-headers-location.patch
Patch3: 003-fix-blocksruntime-headers.patch
Patch4: 004-fix-to-match-system-libobjc2.patch
Patch5: 005-fix-_NSGetExecutablePath.patch
Patch6: 006-fix-backport-NSZone-and-NSAutoreleasePool.patch
Patch7: 007-fix-backport-NSException-and-NSThread.patch
Patch8: 008-fix-linux-unused-declarations.patch
Patch9: 009-fix-enable-cfsslhandler-with-openssl.patch
Patch10: 010-add-installation-support.patch
Patch11: 011-add-real-clean-when-make-clean.patch
Patch12: 012-add-non-fragile-abi-flag.patch
Patch13: 013-add-install-plist-resources-and-pkgconfig.patch
Patch14: 014-add-readme.linux.patch
Patch20: 020-improve-less-warning.patch
Patch21: 021-improve-disable-block-selftest-output.patch

BuildRequires: clang libBlocksRuntime-devel libobjc2-devel openssl-devel

%description
A cross platform implementation of the Apple Cocoa API.

%package devel
Summary: Development headers for libFoundation 
Requires: %{name} = %{version}-%{release}
Requires: libobjc2-devel

%description devel
This package provides headers of libFoundation framework.

%prep
%setup -q -n cocotron
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch20 -p1
%patch21 -p1

%build
export CC=clang
export CXX=clang++
pushd makefiles 
make
popd

%install
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
pushd makefiles 
make install DESTDIR=$RPM_BUILD_ROOT
popd

%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_datadir}/cocotron/Foundation/Resources/*.plist

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/cocotron
%{_includedir}/cocotron/*
%{_libdir}/pkgconfig/cocotron-foundation.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 20150727-2
- Rebuild

* Mon Jul 27 2015 Cjacker <cjacker@foxmail.com>
- git head had merged a lot of contributions.
- update to newest git

* Wed Jul 02 2014 Cjacker <cjacker@gmail.com>
- first build, a lot of patches.
