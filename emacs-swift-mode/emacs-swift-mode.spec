Name: emacs-swift-mode
Version: 0.3.0
Release: 2 
Summary: A major Emacs mode for editing Swift source code
License: GPL
# https://github.com/chrisbarrett/swift-mode
Source0: swift-mode.tar.gz 
Source1: swift-mode-init.el

BuildRequires:emacs
Requires: emacs

BuildArch: noarch

%description
%{summary}

%prep
%setup -n swift-mode

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 swift-mode.el $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/site-start.d/

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
	if ! grep -q swift-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
		echo "(add-hook 'swift-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
	fi
fi ||:

%postun
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
        if grep -q swift-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
                sed -i "s/(add-hook 'swift-mode-hook #'(lambda () (autopair-mode)))//g" /usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        else
                echo "(add-hook 'swift-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        fi
fi ||:

%triggerin -- emacs-autopair
if [ -f "/usr/share/emacs/site-lisp/site-start.d/autopair-init.el" ]; then
        if ! grep -q swift-mode-hook /usr/share/emacs/site-lisp/site-start.d/autopair-init.el; then
                echo "(add-hook 'swift-mode-hook #'(lambda () (autopair-mode)))" >>/usr/share/emacs/site-lisp/site-start.d/autopair-init.el
        fi
fi ||:


%files
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*.el

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 0.3.0-2
- Initial build

