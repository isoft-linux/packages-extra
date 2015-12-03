%global modname nbxmpp
Name:           python-%{modname}
Version:        0.5.3
Release:        2%{?dist}
Summary:        Python library for non-blocking use of Jabber/XMPP
License:        GPLv3
URL:            https://python-nbxmpp.gajim.org/
Source0:        https://python-nbxmpp.gajim.org/downloads/%{modname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       pyOpenSSL
Requires:       pygobject2
Requires:       python-kerberos

%description
python-nbxmpp is a Python library that provides a way for Python applications
to use Jabber/XMPP networks in a non-blocking way.

Features:
- Asynchronous
- ANONYMOUS, EXTERNAL, GSSAPI, SCRAM-SHA-1, DIGEST-MD5, PLAIN, and
    X-MESSENGER-OAUTH2 authentication mechanisms.
- Connection via proxies
- TLS
- BOSH (XEP-0124)
- Stream Management (XEP-0198)

%package doc
Summary:        Developer documentation for %{name}

%description doc
python-nbxmpp is a Python library that provides a way for Python applications
to use Jabber/XMPP networks in a non-blocking way.

This sub-package contains the developer documentation for python-nbxmpp.

%prep
%setup -q -n %{modname}-%{version}

%build
# let's have no executable files in doc/
find doc/ -type f -perm /111 -exec chmod -x {} +
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc COPYING README ChangeLog
%{python2_sitelib}/%{modname}
%{python2_sitelib}/%{modname}-%{version}-*.egg-info

%files doc
%doc COPYING doc/*

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.5.3-2
- Init for isoft4

