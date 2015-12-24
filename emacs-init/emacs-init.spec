%define name	    emacs-init 
%define version	    0.1 
%define release	    4 


#.%{beta}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    Default emacs settings for pure64
License:	GPL
Source0:	000-emacs-init.el	
Source1:        redo+.el
BuildRequires:	emacs	
Requires:	emacs

BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
Default emacs settings for pure64
%prep
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
install -m 0644  %{SOURCE0}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
install -m 0644  %{SOURCE1}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/site-start.d/*.el
%{_datadir}/emacs/site-lisp/*.el
%changelog
* Thu Dec 24 2015 Cjacker <cjacker@foxmail.com> - 0.1-4
- Instead disable backup file, put it under /tmp

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1-3
- Rebuild

