#rust need rust-stage0 to bootstrap.
#we pre-download them and put them in 'dl' folder


%global with_system_llvm 0

Name: rust
Version: 1.1.0
Release: 1
Summary: rust programming language	

Group:   Software/Development/Language
License: Apache 
URL:	 http://www.rust-lang.org	

Source0: https://static.rust-lang.org/dist/rustc-%{version}-src.tar.gz
Source1: http://static.rust-lang.org/stage0-snapshots/rust-stage0-2015-04-27-857ef6e-linux-x86_64-94089740e48167c5975c92c139ae9c286764012f.tar.bz2
Source2: http://static.rust-lang.org/stage0-snapshots/rust-stage0-2015-04-27-857ef6e-linux-i386-0bc8cffdce611fb71fd7d3d8e7cdbfaf748a4f16.tar.bz2

Patch0:	rustc-with-clang-3.7.patch
#warning/error with clang-3.7.
Patch1: rust-fix-llvm-warning.patch

Patch2: rust-1.1.0-install.patch

#only support amd64/x86
ExclusiveArch: x86_64 %{ix86}

BuildRequires: clang
BuildRequires: glibc-devel

%description
Rust is a systems programming language that runs blazingly fast, prevents nearly all segfaults, and guarantees thread safety

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n rustc-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0

#for bootstrap
mkdir dl
cp %{SOURCE1} dl
cp %{SOURCE2} dl

%build
./configure --prefix=%{_prefix} \
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
chmod 755 $RPM_BUILD_ROOT%{_libdir}/rustlib/*/*/*.so

mkdir -p %{buildroot}/%{_docdir}/rust-doc
cp -ra doc/* %{buildroot}/%{_docdir}/rust-doc

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

%changelog
* Tue Jul 28 2015 Cjacker <cjacker@foxmail.com>
- update to 1.1.0
- add ix86 build support.
