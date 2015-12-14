#re-package from atom official binary rpm release.
%define debug_package %{nil}

Name: atom 
Version: 1.3.0
Release: 2
Summary: A hackable text editor for the 21st Century.

License: MIT
URL: https://atom.io
#https://atom.io/download/rpm
Source0: atom.x86_64.rpm
Source1: atom-find-provides.sh
Source2: atom-find-requires.sh

#filter out internal libnode.so
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}


Requires: desktop-file-utils hicolor-icon-theme
 
%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}
pushd %{buildroot}
rpm2cpio %{SOURCE0}|cpio -id

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
        touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/apm
%{_bindir}/atom
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/applications/atom.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 1.3.0-2
- Create package


