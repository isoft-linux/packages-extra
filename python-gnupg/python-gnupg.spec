Name:           python-gnupg
Version:        0.3.7
Release:        3%{?dist}
Summary:        Python module for GnuPG
Group:          Development/Languages
License:        BSD
URL:            http://pythonhosted.org/python-gnupg/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       gnupg

%description
GnuPG bindings for python. This uses the gpg command.

%prep
%setup -q

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc PKG-INFO LICENSE.txt README.rst
%{python_sitelib}/gnupg*.py*
%{python_sitelib}/python_gnupg-%{version}-py*.egg-info

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.3.7-3
- Init for isoft4

