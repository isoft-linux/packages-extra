%global with_python3 1

%global pypi_name netifaces

Name:           python-netifaces
Version:        0.10.4
Release:        3%{?dist}
Summary:        Python library to retrieve information about network interfaces 

License:        MIT
URL:            https://pypi.python.org/pypi/netifaces
Source0:        https://pypi.python.org/packages/source/n/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools


%description
This package provides a cross platform API for getting address information
from network interfaces.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Python library to retrieve information about network interfaces
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
This package provides a cross platform API for getting address information
from network interfaces.
%endif


%prep
%setup -q -n %{pypi_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%Build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python2} setup.py install --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root $RPM_BUILD_ROOT
popd
%endif


%files
%doc README.rst
%{python2_sitearch}/%{pypi_name}-%{version}-*.egg-info/
%{python2_sitearch}/%{pypi_name}.so

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitearch}/%{pypi_name}-%{version}-*.egg-info/
%{python3_sitearch}/%{pypi_name}*.so
%endif

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.10.4-3
- Initial build

