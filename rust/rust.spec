#rust need rust-stage0 to bootstrap.
#we pre-download them and put them in 'dl' folder


%global with_system_llvm 0

Name: rust
Version: 1.9.0
Release: 2 
Summary: rust programming language	

License: Apache 
URL:	 http://www.rust-lang.org	

Source0: https://static.rust-lang.org/dist/rustc-%{version}-src.tar.gz
#see src/snapshots.txt
Source1: http://static.rust-lang.org/stage0-snapshots/rust-stage0-2016-03-18-235d774-linux-x86_64-1273b6b6aed421c9e40c59f366d0df6092ec0397.tar.bz2
Source2: http://static.rust-lang.org/stage0-snapshots/rust-stage0-2016-03-18-235d774-linux-i386-0e0e4448b80d0a12b75485795244bb3857a0a7ef.tar.bz2

Source10: rust-src.sh

Patch0:	rustc-with-clang-3.7.patch
#warning/error with clang-3.7.
Patch1: rust-fix-llvm-warning.patch

Patch2: rust-1.1.0-install.patch

#add isoft tripple
Patch3: rust-add-isoft-tripple.patch

#only support amd64/x86
ExclusiveArch: x86_64 %{ix86}

BuildRequires: clang
BuildRequires: glibc-devel
BuildRequires: curl

%description
Rust is a systems programming language that runs blazingly fast, prevents nearly all segfaults, and guarantees thread safety

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        src
Summary:        Source files for %{name}
Requires:       %{name} = %{version}-%{release}

%description   src
The %{name}-src package contains all sources of rust, intend to used by racer and other utilities.

#filter out any requires/dependencies of sources.
%{?filter_setup:
%filter_provides_in /usr/src/rust
%filter_requires_in /usr/src/rust
%filter_setup
}


%prep
%setup -q -n rustc-%{version}
#%patch0 -p1
#%patch1 -p1
%patch2 -p0

#for bootstrap
mkdir dl
cp %{SOURCE1} dl
cp %{SOURCE2} dl

#setup triplets
#for i686
#cp mk/cfg/i686-unknown-linux-gnu.mk mk/cfg/i686-isoft-linux.mk
#sed -i 's|-gnu||g' mk/cfg/i686-isoft-linux.mk
#sed -i 's|unknown|isoft|g' mk/cfg/i686-isoft-linux.mk
#cp src/librustc_back/target/i686_unknown_linux_gnu.rs src/librustc_back/target/i686_isoft_linux.rs
#sed -i 's|i686-unknown-linux-gnu|i686-isoft-linux|g' src/librustc_back/target/i686_isoft_linux.rs
#
##for x86_64
#cp mk/cfg/x86_64-unknown-linux-gnu.mk mk/cfg/x86_64-isoft-linux.mk
#sed -i 's|-gnu||g' mk/cfg/x86_64-isoft-linux.mk
#sed -i 's|unknown|isoft|g' mk/cfg/x86_64-isoft-linux.mk
#cp src/librustc_back/target/x86_64_unknown_linux_gnu.rs src/librustc_back/target/x86_64_isoft_linux.rs
#sed -i 's|x86_64-unknown-linux-gnu|x86_64-isoft-linux|g' src/librustc_back/target/x86_64_isoft_linux.rs
#
#%patch3 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --enable-clang \
    --enable-optimize \
    --disable-libcpp \
    --enable-docs \
%if %{with_system_llvm}
    --llvm-root=/usr \
%endif
    --release-channel=stable

make all %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}/%{_libdir}/rustlib/components
rm -rf %{buildroot}/%{_libdir}/rustlib/install.log
rm -rf %{buildroot}/%{_libdir}/rustlib/manifest-rustc
rm -rf %{buildroot}/%{_libdir}/rustlib/rust-installer-version
rm -rf %{buildroot}/%{_libdir}/rustlib/uninstall.sh

chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so
#chmod 755 $RPM_BUILD_ROOT%{_libdir}/rustlib/*/*/*.so

mkdir -p %{buildroot}/%{_docdir}/rust-doc
cp -ra doc/* %{buildroot}/%{_docdir}/rust-doc

#install all sources, some utils such as racer need it.
mkdir -p %{buildroot}%{_prefix}/src/rust
tar xf %{SOURCE0} -C %{buildroot}%{_prefix}/src/rust --strip-components=1

pushd %{buildroot}%{_prefix}/src/rust
rm -rf man mk A* L* C* M* R* configure
pushd src
rm -rf llvm rustllvm rt compiler-rt test jemalloc libbacktrace etc doc rust-intaller
popd

#fix perms.
find . -type d|xargs chmod 755 ||:
find . -type f|xargs chmod 644 ||:
popd

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 0755 %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d/rust-src.sh


%check
#too long to run everytime
#make check


%files
%{_bindir}/rust-gdb
%{_bindir}/rustdoc
%{_bindir}/rustc
%{_libdir}/lib*.so
%dir %{_libdir}/rustlib
%{_libdir}/rustlib/*
%{_mandir}/man1/rustc.1.gz
%{_mandir}/man1/rustdoc.1.gz
%{_docdir}/rust
%{_docdir}/rust-doc

%files src
%{_sysconfdir}/profile.d/rust-src.sh
%{_prefix}/src/rust/

%changelog
* Mon Jun 20 2016 Cjacker <cjacker@foxmail.com> - 1.9.0-2
- Update to 1.9.0

* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 1.5.0-2
- Update to 1.5.0

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 1.4.0-4
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.3.0-3
- Rebuild

* Fri Sep 18 2015 Cjacker <cjacker@foxmail.com>
- update to 1.3.0

* Mon Aug 17 2015 Cjacker <cjacker@foxmail.com>
- add src package.

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to 1.2.0

* Tue Jul 28 2015 Cjacker <cjacker@foxmail.com>
- update to 1.1.0
- add ix86 build support.
