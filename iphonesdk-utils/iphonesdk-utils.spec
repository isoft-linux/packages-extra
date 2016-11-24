Name: iphonesdk-utils
Version: 2.1
Release: 3
Summary: iOS development utilities for linux.

License: GPL
URL: https://code.google.com/p/ios-toolchain-based-on-clang-for-linux/
# git clone https://github.com/cjacker/iphonesdk-utils.git
# ./autogen.sh;make dist
Source0: %{name}-%{version}.tar.bz2

BuildRequires: clang libllvm-devel libclang-devel libllvm-static libclang-static
BuildRequires: zlib-devel openssl-devel libxml2-devel libplist-devel

Requires: clang

%description
iOS development utilities for linux.

include:

clangwrapper, wrappers for clang to find SDK and proper compilation args.

ldid, a modified version of ldid with armv7/armv7s support and other changes.

proj2make, a convinent tool to translate xcodeproj Project files to Makefile.

ios-pngcrush, just like pngcrush to optimize png files for iOS.

ios-pngrevert, revert png crushed by ios-pngcrush.

ios-genLocalization, a localization tool based on clang lexer and produce plist string files.

ios-createProject, project templates.

ios-plutil, plist compiler/decompiler.

%prep
%setup -q
%build
export CC=clang
export CXX=clang++
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/ios-clang
%{_bindir}/ios-clang++
%{_bindir}/ios-clang-wrapper
%{_bindir}/ios-createProject
%{_bindir}/ios-genLocalization
%{_bindir}/ios-plutil
%{_bindir}/ios-pngcrush
%{_bindir}/ios-switchsdk
%{_bindir}/ios-xcbuild
%{_bindir}/ldid
%dir %{_datadir}/iPhoneTemplates
%{_datadir}/iPhoneTemplates/*

%changelog
* Thu Nov 24 2016 cjacker - 2.1-3
- Rebuild with new clang/llvm 3.9

* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 2.1-2
- Update to latest version

* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com>
- Initial build


