%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%undefine py2dir
%global py2dir %{_builddir}/dnspython/dnspython-%{version}

%global with_python3 1
%undefine py3dir
%global py3dir %{_builddir}/dnspython/dnspython3-%{version}
%global py3unpack -a 2

Name:           python-dns
Version:        1.12.0GIT465785f
Release:        2%{?dist}
Summary:        DNS toolkit for Python

License:        MIT
URL:            http://www.dnspython.org/
# git snapshots are not on the web
#Source0:        http://www.dnspython.org/kits/%{version}/dnspython-%{version}.tar.gz
Source0:        dnspython-%{version}.tar.gz
%if 0%{?with_python3}
# git snapshots are not on the web
#Source2:        http://www.dnspython.org/kits3/%{version}/dnspython3-%{version}.tar.gz
Source2:        dnspython3-%{version}.tar.gz
%endif

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch

BuildRequires:  python2-devel
# for tests
BuildRequires:  python-crypto

%if 0%{?with_python3}
BuildRequires:  python3-devel
# for tests
BuildRequires:  python3-crypto
%endif

# for DNSSEC support
Requires:       python-crypto

%description
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.

%if 0%{?with_python3}
%package     -n python3-dns
Summary:        DNS toolkit for Python 3

# for DNSSEC support
Requires:       python3-crypto

%description -n python3-dns
dnspython3 is a DNS toolkit for Python 3. It supports almost all
record types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython3 provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.
%endif

%prep
%setup -q -T -c -n dnspython -a 0 %{?py3unpack:%{py3unpack}}

# get rid of Mac goop
find . -name ._\* -delete

# strip executable permissions so that we don't pick up dependencies
# from documentation
find %{py2dir}/examples -type f | xargs chmod a-x
%if 0%{?with_python3}
find %{py3dir}/examples -type f | xargs chmod a-x
%endif

%build
pushd %{py2dir}
%{__python} setup.py build
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}

pushd %{py2dir}
%{__python} setup.py install --skip-build --root %{buildroot}
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%check
pushd %{py2dir}/tests
# skip one test because it queries the network
# dnssec tests fail in RHEL5 Python 2.4 due to the
# lack of some hashes
for py in test_*.py
do
    if [ $py != test_resolver.py ]
    then
        PYTHONPATH=%{buildroot}%{python_sitelib} %{__python} $py
    fi
done
popd

%if 0%{?with_python3}
pushd %{py3dir}/tests
# skip one test because it queries the network
for py in test_*.py
do
    if [ $py != test_resolver.py ]
    then
       PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} $py
    fi
done
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc dnspython-%{version}/{ChangeLog,LICENSE,README,examples}

%{python_sitelib}/*egg-info
%{python_sitelib}/dns

%if 0%{?with_python3}
%files -n python3-dns
%defattr(-,root,root,-)
%doc dnspython3-%{version}/{ChangeLog,LICENSE,README,examples}

%{python3_sitelib}/*egg-info
%{python3_sitelib}/dns
%endif

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 1.12.0GIT465785f-2
- Initial build

