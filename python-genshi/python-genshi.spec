%global with_python3 1

Name:           python-genshi
Version:        0.7
Release:        10%{?dist}
Summary:        Toolkit for stream-based generation of output for the web

License:        BSD
URL:            http://genshi.edgewall.org/

Source0:        http://ftp.edgewall.com/pub/genshi/Genshi-%{version}.tar.gz
Patch0: fix_tests_failure_with_python27.patch  
Patch1: issue566.patch  
Patch2: issue582.patch  
Patch3: issue602.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-babel >= 0.8

%if 0%{?with_python3}
BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
%endif

%description
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web. The major feature is
a template language, which is heavily inspired by Kid.

%if 0%{?with_python3}
%package -n python3-genshi
Summary:        Toolkit for stream-based generation of output for the web
BuildArch:      noarch
Requires:       python3-babel >= 0.8

%description -n python3-genshi
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web. The major feature is
a template language, which is heavily inspired by Kid.
%endif

%prep
%setup0 -q -n Genshi-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

find examples -type f | xargs chmod a-x

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%files
%doc ChangeLog COPYING doc examples README.txt
%{python_sitearch}/Genshi-%{version}-py*.egg-info
%{python_sitearch}/genshi

%if 0%{?with_python3}
%files -n python3-genshi
%doc ChangeLog COPYING doc examples README.txt
%{python3_sitelib}/Genshi-%{version}-py*.egg-info
%{python3_sitelib}/genshi
%endif

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 0.7-10
- Rebuild with python 3.5

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.7-9
- Initial build

