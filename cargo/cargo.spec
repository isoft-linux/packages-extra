Name: cargo
Version: 0.10.0
Release: 2 
Summary: The Rust package manager 	

License: Apache	
URL:	 https://github.com/rust-lang/cargo	
Source0: %{name}-%{version}.tar.gz 

Source1: https://static.rust-lang.org/cargo-dist/cargo-nightly-x86_64-unknown-linux-gnu.tar.gz
Source2: https://static.rust-lang.org/cargo-dist/cargo-nightly-i686-unknown-linux-gnu.tar.gz

#rust-installer
#2015-12-11 git master
Source3: https://github.com/rust-lang/rust-installer/archive/4915c7532533319939c18033c62db875717a4d84.tar.gz

#Pre-downloaded crats required to build cargo
#Generally, every cargo release need update this tarball.
#every crates can be downloaded via:
#https://crates.io/api/v1/crates/[name]/[version]/download
Source4: cargo-crates.tar.gz

Patch0: cargo-0.10.0-crates-local-deps.patch
Patch1: cargo-0.10.0-local-deps.patch

#only support amd64/x86
ExclusiveArch: x86_64 %{ix86}

BuildRequires: rust	
BuildRequires: libcurl-devel openssl-devel libssh2-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: curl
BuildRequires: python

Requires:rust

%description
The Rust package manager.
Cargo downloads your Rust project’s dependencies and compiles your project.

%prep
%setup -q -c
#unpack bootstrap cargo
%ifarch x86_64
tar xf %{SOURCE1} -C .
%endif

%ifarch %{ix86}
tar xf %{SOURCE2} -C .
%endif

#unpack rust-installer
tar xf %{SOURCE3} -C .

#unpack crates
tar xf %{SOURCE4} -C .
pushd cargo-crates
for i in `ls *`;
do
tar xf $i -C ..
done
popd

%patch0 -p1
%patch1 -p1

rm -rf %{name}-%{version}/src/rust-installer/*
tar zxf %{SOURCE3} -C %{name}-%{version}/src/rust-installer/ --strip-components=1

mv cargo-nightly-*-unknown-linux-gnu cargo-prebuilt-bootstrap

%build
pushd %{name}-%{version}
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--disable-verify-install \
	--disable-debug \
	--enable-optimize \
	--local-cargo=`pwd`/../cargo-prebuilt-bootstrap/cargo/bin/cargo

make %{?_smp_mflags}

%install
pushd %{name}-%{version}
CFG_DISABLE_LDCONFIG="true" make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}/%{_datadir}/bash-completion/completions
mv %{buildroot}/usr/etc/bash_completion.d/cargo %{buildroot}/%{_datadir}/bash-completion/completions

#remove rust-lib files, we do not allow user use uninstall.sh scripts to remove cargo.
rm -rf %{buildroot}/%{_libdir}/rustlib
rm -rf %{buildroot}/usr/etc

%files
%{_bindir}/cargo
%{_mandir}/man1/cargo.1*
%{_datadir}/zsh/site-functions/_cargo
%{_datadir}/bash-completion/completions/cargo
%{_docdir}/cargo

%changelog
* Tue Jun 21 2016 Cjacker <cjacker@foxmail.com> - 0.10.0-2
- Update

* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 0.7.0-2
- Update

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 0.6.0-4
- Rebuild with rust 1.4.0 and update related components

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.5.0-3
- Rebuild

* Thu Sep 17 2015 Cjacker <cjacker@foxmail.com>
- update to 0.5.0

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- rebuild with rust-1.2.0
* Wed Jul 29 2015 Cjacker <cjacker@foxmail.com>
- 0.3.0, first build.
