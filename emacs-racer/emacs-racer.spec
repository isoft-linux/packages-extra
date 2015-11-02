Name: emacs-racer
Version: 1.0.2
Release: 4.git
Summary: Allows emacs to use Racer for Rust code completion and navigation.
License: as Emacs 
#https://github.com/racer-rust/emacs-racer
Source0: emacs-racer.tar.gz
Source1: racer-init.el

Requires: emacs emacs-company-mode racer
BuildArch: noarch

%description
Allows emacs to use Racer for Rust code completion and navigation.

%prep
%setup -n emacs-racer

%install
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 racer.el %{buildroot}%{_datadir}/emacs/site-lisp/racer.el
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d/racer-init.el

%files
%{_datadir}/emacs/site-lisp/racer.el
%{_datadir}/emacs/site-lisp/site-start.d/racer-init.el

%changelog
* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-4.git
- Initial build


