#we use official binary release of firefox

%define debug_package %{nil}

%define desktop_file_utils_version 0.9

Summary: Mozilla Firefox Web browser
Name: firefox
Version: 46.0.1
Release: 2
URL: http://www.mozilla.org/projects/firefox
License: MPLv1.1 or GPLv2+ or LGPLv2+
Source0: http://ftp.mozilla.org/pub/firefox/releases/%{version}/linux-x86_64/en-US/firefox-%{version}.tar.bz2
Source20: vendor.js
Source21: firefox.desktop

Source100: find-external-requires

Requires: desktop-file-utils
Requires: firefox-i18n = %{version}
Requires: hunspell
Provides: webclient

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.


%prep
%build
%install
mkdir -p %{buildroot}%{_libdir}/firefox
mkdir -p %{buildroot}%{_bindir}
tar xf %{SOURCE0} -C %{buildroot}%{_libdir}/firefox --strip-components=1

install -Dm644 %{buildroot}%{_libdir}/firefox/browser/icons/mozicon128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/firefox.png
install -Dm644 %{buildroot}%{_libdir}/firefox/browser/chrome/icons/default/default16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/firefox.png
install -Dm644 %{buildroot}%{_libdir}/firefox/browser/chrome/icons/default/default32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/firefox.png
install -Dm644 %{buildroot}%{_libdir}/firefox/browser/chrome/icons/default/default48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/firefox.png

install -Dm644 %{SOURCE20} $RPM_BUILD_ROOT%{_libdir}/firefox/browser/defaults/preferences/vendor.js

install -Dm644 %{SOURCE21} $RPM_BUILD_ROOT%{_datadir}/applications/firefox.desktop

pushd %{buildroot}%{_bindir}
ln -sf /usr/lib/firefox/firefox ./firefox
popd

%clean
rm -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------
%post
touch --no-create %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :

%posttrans
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    fi
fi
update-desktop-database ||:

%files
%defattr(-,root,root,-)
%{_datadir}/applications/*
%dir %{_libdir}/firefox
%{_libdir}/firefox/*
%{_bindir}/firefox
%{_datadir}/icons/hicolor/*/apps/firefox.png

%changelog
* Mon May 16 2016 Cjacker <cjacker@foxmail.com> - 46.0.1-2
- Update to 46.0.1

* Thu Jan 21 2016 Cjacker <cjacker@foxmail.com> - 43.0.4-2
- Update to 43.0.4

* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 43.0-2
- Update to official binary release

* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 42.0-2
- Update to 42.0

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-15
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-14
- Rebuild

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-13
- Update to 41.0.2

* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 41.0

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update 40.0

* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- disable system-cairo in mozconfig, avoid flash plugin blink problem.

* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- add kde integration

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

