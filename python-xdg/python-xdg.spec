Summary: Python library to access freedesktop.org standards
%define real_name pyxdg
Name: python-xdg
Version: 0.25
Release: 2
License: LGPL
URL: http://freedesktop.org/Software/pyxdg
Source: http://www.freedesktop.org/~lanius/pyxdg-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python-devel

Obsoletes: pyxdg <= %{version}-%{release}
Provides: pyxdg = %{version}-%{release}

%description
PyXDG is a python library to access freedesktop.org standards.

%prep
%setup -n %{real_name}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README TODO
%{python_sitearch}/xdg/
%ghost %{python_sitearch}/xdg/*.pyo
%{_libdir}/python2.7/site-packages/pyxdg-0.25-py2.7.egg-info

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.25-2
- Rebuild

