%define realname	    eim
%define version		2.4
%define release	    1

Name:		emacs-%{realname}
Version:	%{version}
Release:	%{release}
Summary:	EIM --- The Emacs Input Method
Group:		Development/Tools	
License:	GPL
URL:        https://github.com/viogus/eim
Source:		viogus-eim-5994240.zip
Source2:	eim-init.el
#if we install it to /usr/share/emacs, normal user can not write to it.
#so we disable it here to avoid write permission denied.
Patch0:     eim-disable-py-save.patch
BuildRequires:	emacs	
Requires:	emacs
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
EIM --- The Emacs Input Method

%prep
%setup -q -c
pushd viogus-eim-5994240
cat %{PATCH0}|patch -p1
popd
%build
%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp
cp -r viogus-eim-5994240 $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/%{realname}
rm -rf $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/%{realname}/*.pl
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
install -m 0644  %{SOURCE2}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/%{realname}
%{_datadir}/emacs/site-lisp/site-start.d/*
%changelog
