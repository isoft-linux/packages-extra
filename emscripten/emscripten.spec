Name: emscripten 
Version: 1.35.12
Release: 3 
Summary: LLVM-based project that compiles C and C++ into highly-optimizable JavaScript in asm.js format

License: Custom
URL: http://kripken.github.io/emscripten-site/

#https://github.com/kripken/
Source0: emscripten-%{version}.tar.gz  
Source1: emscripten-fastcomp-%{version}.tar.gz  
Source2: emscripten-fastcomp-clang-%{version}.tar.gz

#system environments.
Source10: emscripten.sh

#patch to find isoft os toolchain
Patch0: emscripten-clang-lib64-to-lib.patch
Patch1: emscripten-clang-isoft-gcc-toolchain.patch

BuildRequires: cmake libxml2 gcc ninja-build
BuildRequires: glibc-devel ncurses-devel
#Test required
BuildRequires: nodejs

Requires: python nodejs

%description
%{summary}

%prep
%setup -q -c -a1

#setup emscripten llvm fork and put clang in place.
pushd emscripten-fastcomp-%{version}
rm -rf build
mkdir build
rm -rf tools/clang
mkdir -p tools/clang
tar zxf %{SOURCE2} --strip-component=1 -C tools/clang
%patch0 -p1
%patch1 -p1
popd

#ensure python2 is used
#use customized envs to find llvm emscripten fork instead of use the llvm that os shipped.
pushd  emscripten-%{version}
sed '1s|python$|python2|' -i $(find third_party tools -name \*.py) emrun

sed '1s|#!/usr/local/bin/python2|#!env python2|' -i $(find third_party tools -name \*.py)

sed -e "s|getenv('LLVM')|getenv('EMSCRIPTEN_FASTCOMP')|" \
    -e 's|{{{ LLVM_ROOT }}}|/usr/lib/emscripten-fastcomp|' \
    -i tools/settings_template_readonly.py
popd


%build
#build, note the TARGETS settings.
pushd emscripten-fastcomp-%{version}/build
CC=gcc CXX=g++ cmake .. -G Ninja -DPYTHON_EXECUTABLE=/usr/bin/python2 \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_SKIP_RPATH=YES \
    -DLLVM_TARGETS_TO_BUILD="X86;JSBackend" \
    -DLLVM_BUILD_RUNTIME=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DCLANG_INCLUDE_EXAMPLES=OFF \
    -DCLANG_INCLUDE_TESTS=OFF \
    -DLLVM_DEFAULT_TARGET_TRIPLE="x86_64-isoft-linux" \
    -DCLANG_VENDOR="iSoft"

ninja
popd

%install
rm -rf %{buildroot}
# exported variables
install -Dm755 %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d/emscripten.sh

# LLVM-backend, TODO: include only needed tools
pushd emscripten-fastcomp-%{version}
install -Dm644 emscripten-version.txt %{buildroot}%{_libdir}/emscripten-fastcomp/emscripten-version.txt
install -m755 build/bin/* %{buildroot}%{_libdir}/emscripten-fastcomp
popd

# copy structure
pushd emscripten-%{version}
install -d %{buildroot}%{_libdir}/emscripten
cp -rup em* cmake site src system third_party tools %{buildroot}%{_libdir}/emscripten
popd

# remove clutter
rm -rf %{buildroot}%{_libdir}/emscripten-fastcomp/{*-test,llvm-lit}
rm -rf %{buildroot}%{_libdir}/emscripten/*.bat

# docs
install -d %{buildroot}%{_docdir} 
ln -sf %{_libdir}/emscripten/site/source/docs  %{buildroot}%{_docdir}/%{name}

%check
#set HOME to /tmp, emcc will write a .emscripten settings file.
#export HOME=/tmp
#export EMSCRIPTEN=%{buildroot}%{_libdir}/emscripten
#export EMSCRIPTEN_FASTCOMP=%{buildroot}%{_libdir}/emscripten-fastcomp
#export PATH=$EMSCRIPTEN:$PATH
#pushd emscripten-%{version}
##create settings
#emcc -v
##currently , we only run hello world test.
#python tests/runner.py test_hello_world
#popd

%files
%{_sysconfdir}/profile.d/*
%{_libdir}/emscripten
%{_libdir}/emscripten-fastcomp
%{_docdir}/%{name}

%changelog
* Wed Nov 30 2016 cjacker - 1.35.12-3
- Rebuild

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 1.35.12-2
- Update to 1.35.12

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.34.11-3
- Rebuild

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- initial build.
