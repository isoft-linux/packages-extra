%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: CSS Cascading Style Sheets library for Python
Name: python-cssutils
Version: 0.9.9
Release: 7%{?dist}
License: LGPLv3+
URL: http://cthedot.de/cssutils/
Source0: https://bitbucket.org/cthedot/cssutils/downloads/cssutils-%{version}.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Required at runtime for the css* executables
Requires: python-setuptools
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: dos2unix
BuildArch: noarch

%description
A Python package to parse and build CSS Cascading Style Sheets. DOM only, not
any rendering facilities.


%package doc
Summary: Documentation for the CSS Cascading Style Sheets library for Python

%description doc
This is the documentation for python-cssutils, a Python package to parse and
build CSS Cascading Style Sheets.


%prep
%setup -q -n cssutils-%{version}
# Convert all CRLF files, keeping original timestamps
find . -type f -exec dos2unix -k {} \;


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install \
    --single-version-externally-managed \
    -O1 --skip-build --root %{buildroot}
# Don't ship tests. TODO: run tests in check section. 
%{__rm} -rf %{buildroot}/%{python_sitelib}/tests

%clean
%{__rm} -rf %{buildroot}


%files
# The sources have some 2755 mode directories (as of 0.9.5.1), fix here
#defattr(-,root,root,0755)
%defattr(-,root,root,-)
%doc COPYING* README.txt
%{_bindir}/csscapture
%{_bindir}/csscombine
%{_bindir}/cssparse
%{python_sitelib}/cssutils-*.egg-info/
%{python_sitelib}/cssutils/
%{python_sitelib}/encutils/

%files doc
%defattr(-,root,root,-)
%doc examples/


%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.9.9-7
- Initial build

