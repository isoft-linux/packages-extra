#If debuginfo needed, try to modify pre-settings.ini in swift/utils.
%define debug_package %{nil}

%define swift_ver 2.2

%define gitdate 20151212

#swift heavily depend on modified lldb, and it's not LLVM upstream now.
#we had to provided lldb in swift package.
%define lldb_ver 3.8.0

Name: swift
Version: %{swift_ver}
Release: 12.git%{gitdate}
Summary: Swift Programming Language 

License: Apache 2.0 license with a Runtime Library Exception 
URL: http://www.swift.org 
# mkdir -p swift
# cd swift
# git clone https://github.com/apple/swift.git swift
# git clone https://github.com/apple/swift-llvm.git llvm
# git clone https://github.com/apple/swift-clang.git clang
# git clone https://github.com/apple/swift-lldb.git lldb
# git clone https://github.com/apple/swift-cmark.git cmark
# git clone https://github.com/apple/swift-llbuild.git llbuild
# git clone https://github.com/apple/swift-package-manager.git swiftpm
# git clone https://github.com/apple/swift-corelibs-xctest.git
# git clone https://github.com/apple/swift-corelibs-foundation.git
# cd ..
# rm -rf swift/*/.git*
# tar Jcf swift-<data>.tar.xz swift
Source0: swift-%{gitdate}.tar.xz

#Build scripts configs, the most important thing is 'use gold'.
Patch0: 0000-swift-build-config.patch

#Build Preset for iSoft Linux.
Patch1: 0000-swift-isoft-build-preset.patch

#Match our glibc headers.
Patch3: 0001-swift-fix-glibc-header.patch

#Fix python2 detection with newer cmake version.
Patch4: 0002-lldb-fix-python2-detection.patch

#inherent from our llvm/clang build
Patch5: 0003-llvm-add-test-hasSSE41-detection-pentium-dual-core.patch
#prefer lib instead of lib64
Patch6: 0004-clang-lib64-to-lib.patch
#refer to patch filename.
Patch7: 0005-clang-add-our-own-gcc-toolchain-tripplet-to-clang-search-path.patch

#add GCC libstdc++ abi_tag support
Patch10: swift-clang-3.8-add-gcc-abi_tag.patch
Patch11: swift-clang-3.8-add-missing-header.patch 
Patch12: swift-clang-3.8-abi_tag-fix-segfault-when-build-libcxx.patch

BuildRequires: clang
BuildRequires: swig 
BuildRequires: cmake ninja-build
BuildRequires: python python-sphinx python3
BuildRequires: bison flex 
BuildRequires: zip
BuildRequires: doxygen
BuildRequires: tar
BuildRequires: pkgconfig
#package need it.
BuildRequires: rsync

BuildRequires: python-devel
BuildRequires: libedit-devel
BuildRequires: libxml2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-headers
BuildRequires: libffi-devel
BuildRequires: libstdc++-devel
BuildRequires: binutils-devel
BuildRequires: ncurses-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libbsd-devel
BuildRequires: zlib-devel
BuildRequires: libuuid-devel
BuildRequires: libicu-devel
BuildRequires: sqlite-devel
 
#swift repl required.
Requires: swift-lldb = %{lldb_ver}-%{release}

%description
Swift is a general-purpose programming language built using a modern approach to safety, performance, and software design patterns.

The goal of the Swift project is to create the best available language for uses ranging from systems programming, to mobile and desktop apps, scaling up to cloud services. 

Most importantly, Swift is designed to make writing and maintaining correct programs easier for the developer. 

%package -n swift-lldb
Version: %{lldb_ver}
Summary: LLDB is a next generation, high-performance debugger
Requires: swift-liblldb = %{lldb_ver}-%{release}
Provides: lldb = %{lldb_ver}-%{release}

%description -n swift-lldb
LLDB is a next generation, high-performance debugger. It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project, such as the Clang expression parser and LLVM disassembler.

%package -n swift-liblldb
Version: %{lldb_ver}
Summary: Libraries for develop program with liblldb
Provides: liblldb = %{lldb_ver}-%{release}

%description -n swift-liblldb
This package contains libraries for develop program with liblldb.

%package -n swift-liblldb-devel
Version: %{lldb_ver}
Summary: Header files for lldb library.
Requires: swift-liblldb = %{lldb_ver}-%{release}
Provides: liblldb-devel = %{lldb_ver}-%{release}

#we provided this package before
Obsoletes: liblldb-static <= %{lldb_ver}

%description -n swift-liblldb-devel
This package contains header files for lldb library.

%prep
%setup -q -n %{name}
%patch0 -p1 -d swift
%patch1 -p1 -d swift
%patch3 -p1 -d swift
%patch4 -p1 -d lldb
%patch5 -p1 -d llvm
%patch6 -p1 -d clang 
%patch7 -p1 -d clang 

#abi_tag support
%patch10 -p1 -d clang
%patch11 -p1 -d clang
%patch12 -p1 -d clang

%build
mkdir -p %{_builddir}/swift-%{swift_ver}-%{release}-root

./swift/utils/build-script \
    --preset=buildbot_linux_isoft \
    install_destdir=%{_builddir}/swift-%{swift_ver}-%{release}-root \
    installable_package=%{_builddir}/swift-%{swift_ver}-%{release}-root/swift-%{swift_ver}-isoft.tar.gz

%install
tar zxf %{_builddir}/swift-%{swift_ver}-%{release}-root/swift-%{swift_ver}-isoft.tar.gz -C %{buildroot}

#remove empty dir
rm -rf %{buildroot}/usr/local

%post -n swift-liblldb -p /sbin/ldconfig
%postun -n swift-liblldb -p /sbin/ldconfig

%files
%{_bindir}/swift
%{_bindir}/swiftc
%{_bindir}/swift-autolink-extract
%{_bindir}/repl_swift
%{_bindir}/swift-build
%{_bindir}/swift-demangle
%{_bindir}/swift-build-tool
%dir %{_libdir}/swift
%{_libdir}/swift/*
%dir %{_libdir}/swift_static
%{_libdir}/swift_static/*
%{_mandir}/man1/swift.1*

%files -n swift-lldb
%defattr(-,root,root)
%{_bindir}/lldb
%{_bindir}/lldb-3.*
%{_bindir}/lldb-mi
%{_bindir}/lldb-mi-*
%{_bindir}/lldb-server
%{_bindir}/lldb-server-3.*
%{_bindir}/lldb-argdumper
%{python_sitearch}/lldb
%{python_sitearch}/readline.so

%files -n swift-liblldb
%defattr(-,root,root)
%dir %{_libdir}/lldb
%{_libdir}/lldb/*
%{_libdir}/liblldb.so
%{_libdir}/liblldb.so.3*

%files -n swift-liblldb-devel
%defattr(-,root,root)
%{_includedir}/lldb

%changelog
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 2.2-12.git20151212
- Update and rebuild with llvm 3.7.1

* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 2.2-9.git20151211
- Update to 20151211 git

* Thu Dec 10 2015 Cjacker <cjacker@foxmail.com> - 2.2-8.git20151210
- Update to 20151210 git

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 2.2-7.git20151209
- Update to 2015 1209 git

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 2.2-6.git20151208
- Update to 20151208 git

* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 2.2-5.git20151207
- Update

* Sun Dec 06 2015 Cjacker <cjacker@foxmail.com> - 2.2-4.git20151206
- Rebuild
- Add gcc abi_tag patches(#10, #11, #12).

* Sun Dec 06 2015 Cjacker <cjacker@foxmail.com> - 2.2-3.git20151206
- Update to 20151206 latest git

* Fri Dec 04 2015 Cjacker <cjacker@foxmail.com> - 2.2-2.git20151204
- Initial build.
- Add 'build-linux-isoft' as build presettings.
- disable package test after build.
- switch to gold
- other various fixes. 
