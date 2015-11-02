Name: emacs-company-mode
Version: 0.8.12 
Release: 3
Summary: Text completion framework for Emacs
License: as Emacs 
#https://github.com/company-mode/company-mode
Source0: company-mode-0.8.12.tar.gz 
Requires: emacs
BuildArch: noarch

%description
Company is a text completion framework for Emacs.

%prep
%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mv $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/company-mode-%{version} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/company-mode

%files
%{_datadir}/emacs/site-lisp/company-mode

%changelog
* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 0.8.12-3
- Initial build

