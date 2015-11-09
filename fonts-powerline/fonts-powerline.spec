%global fontname powerline 
Name: fonts-%{fontname}
Version: 20151107 
Release: 2%{?dist}
Summary: Pre-patched and adjusted fonts for usage with the Powerline plugin

License: See README.rst 

URL: https://github.com/powerline/fonts 

#https://github.com/powerline/fonts
Source0:        fonts.tar.gz

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
%{summary}

%prep
%setup -q -c

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts/powerline

cp -r fonts/* $RPM_BUILD_ROOT%{_datadir}/fonts/powerline
rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts/powerline/install.sh
rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts/powerline/README.rst

%files
%defattr(-,root,root)
%doc fonts/README.rst
%{_datadir}/fonts/powerline

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 20151107-2
- Initial build


