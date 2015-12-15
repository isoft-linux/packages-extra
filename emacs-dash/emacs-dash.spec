Name: emacs-dash 
Version: 2.12.1
Release: 2.git
Summary: A modern list library for Emacs 

License: OpenSource 
URL: https://github.com/magnars/dash.el
Source0: dash.el.tar.gz

BuildArch: noarch

%description
%{summary}

%prep
%setup -q -n dash.el
%build
%install
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
install -m0644 *.el %{buildroot}%{_datadir}/emacs/site-lisp

%files
%{_datadir}/emacs/site-lisp/*.el

%changelog
* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 2.12.1-2.git
- Initial build


