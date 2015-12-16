Name: emacs-elixir
Version: 2.2.8
Release: 2.git
Summary: Provides font-locking, indentation and navigation support for the Elixir programming language.
License: as Emacs 
# https://github.com/elixir-lang/emacs-elixir
Source0: %{name}.tar.gz
 
Source1: elixir-init.el

Patch0: remove-pkg-info.el-require.patch

Requires: emacs
BuildArch: noarch

%description
%{summary}

%prep
%setup -n emacs-elixir
%patch0 -p1

%install
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 *.el %{buildroot}%{_datadir}/emacs/site-lisp
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d/elixir-init.el

%files
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*-init.el

%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 2.2.8-2.git
- Initial build



