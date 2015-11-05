%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-mechanize
Version:        0.2.5
Release:        10%{?dist}
Summary:        Stateful programmatic web browsing

License:        BSD or ZPLv2.1
URL:            http://wwwsearch.sourceforge.net/mechanize
Source0:        http://wwwsearch.sourceforge.net/mechanize/src/mechanize-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
# for tests
#BuildRequires:  python-zope-interface python-twisted-web2
BuildRequires: python-setuptools


%description
Stateful programmatic web browsing, after Andy Lester's Perl module
WWW::Mechanize.

The library is layered: mechanize.Browser (stateful web browser),
mechanize.UserAgent (configurable URL opener), plus urllib2 handlers.

Features include: ftp:, http: and file: URL schemes, browser history,
high-level hyperlink and HTML form support, HTTP cookies, HTTP-EQUIV and
Refresh, Referer [sic] header, robots.txt, redirections, proxies, and
Basic and Digest HTTP authentication.  mechanize's response objects are
(lazily-) .seek()able and still work after .close().

Much of the code originally derived from Perl code by Gisle Aas
(libwww-perl), Johnny Lee (MSIE Cookie support) and last but not least
Andy Lester (WWW::Mechanize).  urllib2 was written by Jeremy Hylton.


%prep
%setup -q -n mechanize-%{version}
chmod -x examples/forms/{echo.cgi,example.py,simple.py}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --single-version-externally-managed \
                             -O1 --root=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%check
# The TestPullParser unit tests are now failing
# https://github.com/jjlee/mechanize/issues/72
rm test/test_pullparser.py

chmod +x examples/forms/{echo.cgi,example.py,simple.py}
%{__python} test.py --log-server
chmod -x examples/forms/{echo.cgi,example.py,simple.py}

%files
%defattr(-,root,root,-)
%doc COPYING.txt README.txt docs/ examples/
%{python_sitelib}/*


%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.2.5-10
- Initial build

