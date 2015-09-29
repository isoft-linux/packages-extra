Name: racer 
Version: 1.0.0 
Release: 3 
Summary: Code completion for Rust

License: MIT
URL:	 https://github.com/phildawes/racer
Source0: %{name}-%{version}.tar.gz 

#predownload carets
Source4: racer-crates.tar.gz

#company-mode is needed by emacs racer mode
Source10: company-mode-0.8.12.tar.gz
Source11: racer-init.el

Patch1: racer-1.0.0-local-deps.patch
Patch2: racer-1.0.0-local-deps2.patch

#only support amd64/x86
ExclusiveArch: x86_64 %{ix86}

BuildRequires: rust	

Requires:rust
Requires:rust-src

%description
The Rust package manager.
Cargo downloads your Rust project’s dependencies and compiles your project.

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
%patch2 -p1

%build
pushd %{name}-%{version}
cargo build --release
popd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d

pushd %{name}-%{version}
install -m 0755 target/release/racer %{buildroot}%{_bindir}/racer
popd

#setup emacs plugin
tar xf %{SOURCE10} -C %{buildroot}%{_datadir}/emacs/site-lisp
install -m 0644 %{name}-%{version}/editors/emacs/racer.el %{buildroot}%{_datadir}/emacs/site-lisp/racer.el
install -m 0644 %{SOURCE11} %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d/racer-init.el

%files
%{_bindir}/racer
%{_datadir}/emacs/site-lisp/racer.el
%{_datadir}/emacs/site-lisp/company-mode-*
%{_datadir}/emacs/site-lisp/site-start.d/racer-init.el

%changelog
* Fri Sep 18 2015 Cjacker <cjacker@foxmail.com>
- rebuild with rust 1.3.0
* Mon Aug 17 2015 Cjacker <cjacker@foxmail.com>
- initial build.
