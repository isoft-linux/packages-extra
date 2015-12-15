Name: emacs-company-mode
Version: 0.8.12 
Release: 4
Summary: Text completion framework for Emacs
License: as Emacs 
#https://github.com/company-mode/company-mode
Source0: company-mode.tar.gz 
Requires: emacs
BuildArch: noarch

%description
Company is a text completion framework for Emacs.

%prep
%install
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/company-mode
tar xf %{SOURCE0} -C %{buildroot}%{_datadir}/emacs/site-lisp/company-mode --strip-components=1

rm -rf %{buildroot}%{_datadir}/emacs/site-lisp/company-mode/.git*

%files
%{_datadir}/emacs/site-lisp/company-mode

%changelog
* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 0.8.12-4
- Update

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 0.8.12-3
- Initial build

