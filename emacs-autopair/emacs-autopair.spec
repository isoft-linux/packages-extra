Name:	    emacs-autopair
Version:	0.1
Release:    2	
Summary:    Another stab at making braces and quotes pair like in TextMate	
License:	GPL
Source0:	autopair.el
Source1:    autopair-init.el
BuildRequires:	emacs
Requires:	emacs
BuildArch: noarch

BuildRoot:	%{_tmppath}/%{realname}-%{version}-%{release}

%description
Another stab at making braces and quotes pair like in TextMate
%prep
%install
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d/
%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
/usr/share/emacs/site-lisp/*.el
/usr/share/emacs/site-lisp/site-start.d/*.el

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1-2
- Rebuild

