Name: emacs-rust-mode
Version: 0.1
Release: 1	
Summary: A major Emacs mode for editing Rust source code
License: GPL
#git clone https://github.com/rust-lang/rust-mode
Source0: rust-mode.tar.gz 
Source1: rust-mode-init.el
BuildRequires:emacs
Requires: emacs

%description
%{summary}

%prep
%setup -n rust-mode

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 rust-mode.el $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/site-start.d/

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
	if ! grep -q rust-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
		echo "(add-hook 'rust-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
	fi
fi ||:

%postun
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
        if grep -q rust-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
                sed -i "s/(add-hook 'rust-mode-hook #'(lambda () (autopair-mode)))//g" /usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        else
                echo "(add-hook 'rust-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        fi
fi ||:

%triggerin -- emacs-autopair
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
        if ! grep -q rust-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
                echo "(add-hook 'rust-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        fi
fi ||:


%files
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*.el

%changelog
* Fri Jul 31 2015 Cjacker <cjacker@foxmail.com>
- initial build
