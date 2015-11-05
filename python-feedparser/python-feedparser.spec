%global with_python3 1

%global with_docpkg 1

%global srcname feedparser
%global tag     .post1

Name:           python-feedparser
Version:        5.2.0
Release:        2%{?dist}
Summary:        Parse RSS and Atom feeds in Python

License:        BSD
URL:            https://github.com/kurtmckee/feedparser
Source0:        https://pypi.python.org/packages/source/f/%{srcname}/%{srcname}-%{version}%{tag}.tar.bz2
# only for EPEL5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

# optional import at run-time, but is likely installed because other
# python module packages depend on it, too
# no failing tests on 2013-03-09 with python-chardet-2.0.1
BuildRequires: python-chardet
Requires: python-chardet

## TODO: Decide on these, also with regard to explicit "Requires".
## Optional imports at run-time and influence the test-suite, too,
## and causes additional tests to fail.
#
#BuildRequires:  python-BeautifulSoup
#  usage removed in > 5.1.3
#
## the preferred XML parser
#BuildRequires:  libxml2-python

## TODO: python3-chardet BR and Req
# fixes included in > 5.1.3

# shows that for Python 3 the test-suite fails early with
#   ImportError: No module named 'BaseHTTPServer'
Patch0: feedparser-5.1.3-tests-py3.patch


%description
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Parse RSS and Atom feeds in Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%description -n python3-%{srcname}
Universal Feed Parser is a Python module for downloading and parsing 
syndicated feeds. It can handle RSS 0.90, Netscape RSS 0.91, 
Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94, RSS 1.0, RSS 2.0, 
Atom 0.3, Atom 1.0, and CDF feeds. It also parses several popular extension 
modules, including Dublin Core and Apple's iTunes extensions.
%endif

%if 0%{?with_docpkg}
%package doc
BuildRequires: python-sphinx
BuildArch: noarch
Summary: Documentation for the Python feedparser

%description doc
This documentation describes the behavior of Universal Feed Parser %{version}. 

The documentation is also included in source form (Sphinx ReST).
%endif


%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?with_python3}
cp -a . %{py3dir}
pushd %{py3dir}
%patch0 -p1
popd
%endif

find -type f -exec sed -i 's/\r//' {} ';'
find -type f -exec chmod 0644 {} ';'


%build
%{__python2} setup.py build

%if 0%{?with_docpkg}
# build documentation
rm -rf __tmp_docs ; mkdir __tmp_docs
sphinx-build -b html -d __tmp_docs/ docs/ __tmp_docs/html/
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# only for EPEL5
rm -rf %{buildroot}

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif


%check
pushd feedparser
PYTHONPATH=%{buildroot}%{python2_sitelib} %{__python2} feedparsertest.py || :
popd
%if 0%{?with_python3}
pushd %{py3dir}/feedparser
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} feedparsertest.py || :
popd
%endif


# only for EPEL5
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst NEWS
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE README.rst NEWS
%{python3_sitelib}/*
%endif

%if 0%{?with_docpkg}
%files doc
%doc LICENSE __tmp_docs/html/
# the original Sphinx ReST tree
%doc docs
%endif

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 5.2.0-2
- Initial build

