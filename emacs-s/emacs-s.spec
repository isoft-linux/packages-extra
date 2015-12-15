Name: emacs-s
Version: 1.10.0
Release: 2.git
Summary: The long lost Emacs string manipulation library.
License: OpenSource 
URL: https://github.com/magnars/s.el
Source0: s.el.tar.gz

BuildArch: noarch

%description
%{summary}

%prep
%setup -q -n s.el
%build
%install
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
install -m0644 *.el %{buildroot}%{_datadir}/emacs/site-lisp

%files
%{_datadir}/emacs/site-lisp/*.el

%changelog
* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2.git
- Initial build



