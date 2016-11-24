Name:  cctools
Version: 886 
Release: 2
Summary: Apple cctools port for Linux

License: APPLE PUBLIC SOURCE LICENSE
URL: https://code.google.com/p/ios-toolchain-based-on-clang-for-linux

#git clone https://github.com/tpoechtrager/cctools-port.git
#./package.sh
Source0: cctools-886-ld64-264.3.102_84ce22d.tar.xz

BuildRequires: clang llvm libllvm-devel xar-devel libuuid-devel

Requires: clang llvm 

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n cctools-886-ld64-264.3.102_84ce22d

%build
cp -r cctools cctools-ios
cp -r cctools cctools-x86_64

pushd cctools-ios
%configure \
    --target=arm-apple-darwin11 \
    --program-prefix="arm-apple-darwin11-" \
    --enable-lto-support
make %{?_smp_mflags}
popd

pushd cctools-x86_64
%configure \
    --target=x86_64-apple-darwin11 \
    --program-prefix="x86_64-apple-darwin11-" \
    --enable-lto-support
make %{?_smp_mflags}
popd

%install
pushd cctools-ios
make install DESTDIR=%{buildroot}
popd

pushd cctools-x86_64
make install DESTDIR=%{buildroot}
popd

%files
%{_bindir}/arm-apple-darwin11-*
%{_bindir}/x86_64-apple-darwin11-*
%dir %{_libexecdir}/as
%{_libexecdir}/as/*/as

%changelog
* Thu Nov 24 2016 cjacker - 886-2
- Update to 886

* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 877.5-2
- Initial build


