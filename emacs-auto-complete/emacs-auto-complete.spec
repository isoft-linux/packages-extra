Name: emacs-auto-complete
Version: 1.4
Release: 4 
Summary: emacs c/c++/objc codes auto complete based on clang.
URL: http://cx4a.org/software/auto-complete	
License: GPL
#do not use 1.3.1, conflicts with autopair mode.
Source0: auto-complete-%{version}.tar.bz2
#https://github.com/Golevka/emacs-clang-complete-async
Source1: emacs-clang-complete-async-master.zip
Source2: auto-complete-init.el 
Patch0: emacs-clang-complete-async-remove-flymake.patch
Patch1: emacs-clang-complete-async-with-macros-completion.patch
Patch2: emacs-clang-complete-async-run-only-once.patch
Patch3: emacs-clang-complete-async-auto-find-pch.patch
Patch4: emacs-clang-complete-fix-include-pch-crash.patch
Patch5: emacs-clang-complete-miss-header.patch

BuildRequires:	emacs libclang-devel
Requires:	emacs emacs-init libclang
BuildRoot:	%{_tmppath}/%{realname}-%{version}-%{release}

%description
Codes auto complete for emacs based on clang.
%prep
%setup -q -c -a1 
pushd emacs-clang-complete-async-master
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i "s@stdc++@c++@g" Makefile
popd
%build
pushd auto-complete-%{version}
make
popd
pushd emacs-clang-complete-async-master
make CC=clang
popd
 
%install
mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/auto-complete
mkdir -p $RPM_BUILD_ROOT/usr/bin

pushd auto-complete-%{version}
make install DIR=$RPM_BUILD_ROOT/usr/share/emacs/site-lisp/auto-complete
popd

pushd emacs-clang-complete-async-master
install -m 0755 clang-complete $RPM_BUILD_ROOT/usr/bin
install -m 0644 auto-complete-clang-async.el $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/ 
popd

mkdir -p $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d/
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/emacs/site-lisp/site-start.d/
%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
/usr/bin/*
/usr/share/emacs/site-lisp/auto-complete
/usr/share/emacs/site-lisp/*.el
/usr/share/emacs/site-lisp/site-start.d/*.el

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.4-4
- Rebuild

* Tue Oct 27 2015 cjacker - 1.4-3
- Rebuild with new llvm

