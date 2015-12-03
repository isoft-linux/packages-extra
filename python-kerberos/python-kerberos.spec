%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:           python-kerberos
Version:        1.1
Release:        20%{?dist}
Summary:        A high-level wrapper for Kerberos (GSSAPI) operations

License:        ASL 2.0
URL:            http://trac.calendarserver.org/projects/calendarserver/browser/PyKerberos
# Pull from SVN
# svn export http://svn.calendarserver.org/repository/calendarserver/PyKerberos/tags/release/PyKerberos-1.1/ python-kerberos-1.1
# tar czf python-kerberos-%{version}.tar.gz python-kerberos-%{version}
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  krb5-devel
BuildRequires:  python-setuptools

Patch0: PyKerberos-delegation.patch
Patch1: PyKerberos-version.patch
Patch2: PyKerberos-inquire.patch
Patch3: PyKerberos-gsswrap.patch

%description
This Python package is a high-level wrapper for Kerberos (GSSAPI) operations.
The goal is to avoid having to build a module that wraps the entire
Kerberos.framework, and instead offer a limited set of functions that do what
is needed for client/serverKerberos authentication based on
<http://www.ietf.org/rfc/rfc4559.txt>.

Much of the C-code here is adapted from Apache's mod_auth_kerb-5.0rc7.


%prep
%setup -q

%patch0 -p1 -b .delegation
%patch1 -p1 -b .version
%patch2 -p1 -b .inquire
%patch3 -p1 -b .gsswrap

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt test.py
%license LICENSE
%{python_sitearch}/*


%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 1.1-20
- update release

* Thu Dec 03 2015 sulit <sulitsrc@gmai.com> - 1.1-19
- Init for isoft4

