Name: firefox-i18n
Version: 41.0
Release: 1
Summary: Language pack for firefox
License:	MPL
URL:		http://download.cdn.mozilla.net/pub/firefox/releases/33.0.2/linux-x86_64/xpi
#this is a tarball of all xpi files.
Source0:    %{name}-%{version}.tar.gz

Requires:   firefox	= %{version}

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
* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 41.0

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 40.0

* Tue Jul 07 2015 Cjacker <cjacker@foxmail.com>
- update to 39.0
