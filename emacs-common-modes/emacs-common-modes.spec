%define with_internal_cedet 0 
%define debug_package %{nil}
Name:           emacs-common-modes 
Version:        0.1 
Release:        2
Summary:        Some basic modes for emacs 

License:        GPL
#this is a modified version of rpm-spec to fix readonly buffer bugs.
Source1:  rpm-spec-mode.el
Source2:  csharp-mode.el
#php mode 1.5.0
#http://download.sourceforge.net/php-mode/
Source3:  php-mode.el 
Source4:  ssl.el
Source5:  igrep.el
 
Source100: emacs-modes-init.el
Source101: c-init.el
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}
Requires: emacs emacs-init
BuildRequires: emacs

BuildArch: noarch

%description
Some basic modes for emacs

%prep

%Build
%install
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
#rpm spec mode
install -m 644 %{SOURCE1}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
#csharp mode
install -m 644 %{SOURCE2}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
#php mode
install -m 644 %{SOURCE3}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
#ssl functions 
install -m 644 %{SOURCE4}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp
#igrep mode
install -m 644 %{SOURCE5}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp

# modes init files.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 644 %{SOURCE100}  $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 644 %{SOURCE101}  $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/emacs/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1-2
- Rebuild

