%global srcname python-dateutil
Name:           python-dateutil15
Version:        1.5
Release:        8%{?dist}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python
URL:            http://labix.org/python-dateutil
Source0:        http://labix.org/download/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:         python-dateutil-1.5-system-zoneinfo.patch
BuildArch:      noarch
BuildRequires:  python-devel,python-setuptools

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.  This is backwards compatibility version 
is parallel-installable with dateutil 2.x .

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python} setup.py bdist_egg

%install
mkdir -p %{buildroot}%{python_sitelib}
easy_install -m --prefix %{buildroot}%{_usr} dist/*.egg

chmod -x %{buildroot}%{python_sitelib}/python_dateutil-%{version}-py%{python2_version}.egg/dateutil/*.py 
chmod -x %{buildroot}%{python_sitelib}/python_dateutil-%{version}-py%{python2_version}.egg/dateutil/zoneinfo/__init__.py

%files
%doc example.py LICENSE NEWS README
%{python_sitelib}/python_dateutil-%{version}-py%{python2_version}.egg
%exclude %{python_sitelib}/dateutil/zoneinfo/zoneinfo-2010g.tar.gz


%changelog
* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
