Name: racer 
Version: 1.1.0 
Release: 6.git
Summary: Code completion for Rust

License: MIT
URL:	 https://github.com/phildawes/racer
#https://github.com/phildawes/racer
Source0: %{name}.tar.gz 

#predownload carets
Source4: racer-crates.tar.gz

Patch1: racer-1.1.0-local-deps.patch

#only support amd64/x86
ExclusiveArch: x86_64 %{ix86}

BuildRequires: rust cargo

Requires: rust
#racer use rust source to provide completions.
Requires: rust-src

%description
Code completion for Rust

%prep
%setup -q -c
#unpack carets
tar xf %{SOURCE4} -C .
pushd racer-crates
for i in `ls *`;
do
tar xf $i -C ..
done
popd

%patch1 -p1

%build
pushd %{name}
cargo build --release
popd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d

pushd %{name}
install -m 0755 target/release/racer %{buildroot}%{_bindir}/racer
popd

%files
%{_bindir}/racer

%changelog
* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 1.1.0-6.git
- Update to latest git, fix all warnings

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 1.0.0-5
- Rebuild with rust 1.4.0

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.0.0-4
- Rebuild

* Fri Sep 18 2015 Cjacker <cjacker@foxmail.com>
- rebuild with rust 1.3.0
* Mon Aug 17 2015 Cjacker <cjacker@foxmail.com>
- initial build.
