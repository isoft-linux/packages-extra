Name: iphonesdk-utils
Version: 2.0
Release: 2
Summary: iOS development utilities for linux.

License: GPL
URL: https://code.google.com/p/ios-toolchain-based-on-clang-for-linux/
Source0: %{name}-%{version}.tar.gz
Source1: ldid.tar.gz

Patch0: iphonesdk-utils-fix-build-with-llvm37.patch
Patch1: iphonesdk-utils-genLocalization-fix-search-header-with-llvm37.patch
Patch2: iphonesdk-utils-default-to-9.2-sdk-and-arch-to-arm64.patch

BuildRequires: clang libllvm-devel libclang-devel
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

mkdir -p ldid2
tar zxf %{SOURCE1} -C ldid2

%build
export CC=clang
export CXX=clang++
./autogen.sh
%configure
make %{?_smp_mflags}

pushd ldid2/ldid
make
popd

%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_bindir}/ldid
install -m0755 ldid2/ldid/ldid %{buildroot}%{_bindir}/ldid


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
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com>
- Initial build


