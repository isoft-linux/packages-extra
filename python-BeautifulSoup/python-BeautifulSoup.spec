%global oname   BeautifulSoup

Name:           python-BeautifulSoup
Epoch:          1
Version:        3.2.1
Release:        10%{?dist}
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
License:        BSD
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-%{version}.tar.gz
Provides:       python-beautifulsoup = %{epoch}:%{version}-%{release}
BuildRequires:  python-devel
BuildArch:      noarch

%description
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python2} setup.py build
%{__python2} -c 'import %{oname} as bs; print bs.__doc__' > COPYING
touch -r %{oname}.py COPYING

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
#Files installed by error
rm -rf %{buildroot}%{_bindir}

%check
%{__python2} BeautifulSoupTests.py

%files
%doc COPYING
%{python_sitelib}/%{oname}.py*
%exclude %{python_sitelib}/%{oname}Tests.py*
%{python_sitelib}/%{oname}-%{version}-py*.egg-info

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 1:3.2.1-10
- Initial build

