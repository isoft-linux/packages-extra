%define gitname     yasnippet
%define beta	    %nil	
%define realname    yasnippet
%define version	    0.8.1	
%define release	    2


Name:		emacs-%{realname}
Version:	%{version}
Release:	%{release}
Summary:	Yet another snippet extension for Emacs.
License:	GPL
URL:        	https://github.com/capitaomorte/yasnippet
#git clone --recursive https://github.com/capitaomorte/yasnippet
Source:		%{gitname}.tar.gz
Source2:	%{realname}-init.el
Patch0:     	yasnippet-c-mystyle.patch
BuildRequires:	emacs	
Requires:	emacs
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

BuildArch: noarch

%{?filter_setup:
%filter_requires_in /usr/share/emacs
%filter_setup
}


%description
Yet another snippet extension for Emacs.
%prep
%setup -q -c
pushd %{gitname}
find . -name .git|xargs rm -rf
cat %{PATCH0}|patch -p1
popd
%build
%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp
cp -r %{gitname} $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/%{realname}
#rm -rf $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/%{realname}/*.pl

#tar zxvf %{SOURCE1} -C $RPM_BUILD_ROOT/%{_datadir}/emacs/site-lisp/yasnippet/snippets/objc-mode/ 

mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d
install -m 0644  %{SOURCE2}  $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_datadir}/emacs/site-lisp/%{realname}
%{_datadir}/emacs/site-lisp/site-start.d/*
%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.8.1-2
- Rebuild

