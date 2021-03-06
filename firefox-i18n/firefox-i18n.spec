%define debug_package %{nil}

Name: firefox-i18n
Version: 50.0.2 
Release: 2
Summary: Language pack for firefox
License: MPL
URL: http://download.cdn.mozilla.net/pub/firefox/releases/%{version}/linux-x86_64/xpi
#this is a tarball of all xpi files.
#wget -c -r -nd -np -k <URL>
Source0: %{name}-%{version}.tar.gz

%description
Language pack for firefox

%prep
%setup -c -q

%build
%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/firefox/browser/extensions/
for i in *.xpi
do
    name=`basename -s .xpi $i`
    install -m0644 $i $RPM_BUILD_ROOT%{_libdir}/firefox/browser/extensions/langpack-$name@firefox.mozilla.org.xpi
done

%files
%{_libdir}/firefox/browser/extensions/langpack-*@firefox.mozilla.org.xpi

%changelog
* Thu Dec 08 2016 cjacker - 50.0.2-2
- Update to 50.0.2

* Mon May 16 2016 Cjacker <cjacker@foxmail.com> - 46.0.1-2
- Update to 46.0.1

* Tue Feb 16 2016 Cjacker <cjacker@foxmail.com> - 44.0.2-3
- Update to 44.0.2

* Thu Jan 21 2016 Cjacker <cjacker@foxmail.com> - 43.0.4-2
- Update to 43.0.4

* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 43.0-2
- Update to 43.0 xpis

* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 42.0-2
- Update to 42.0

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 41.0-2
- Rebuild

* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 41.0

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 40.0

* Tue Jul 07 2015 Cjacker <cjacker@foxmail.com>
- update to 39.0
