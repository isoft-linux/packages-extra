Name:    lokalize
Summary: Computer-aided translation system
Version: 15.12.0
Release: 3

License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdesdk/lokalize
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz
Patch0: lokalize-tune-desktop.patch

#start lokalize, press "Open" from toolbar and open a po file, it will segfault.
Patch1: always-add-mdi-window-first-to-avoid-crash.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros

BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kross-devel
BuildRequires: kf5-sonnet-devel
BuildRequires: kf5-kcrash-devel

BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(Qt5Widgets) pkgconfig(Qt5DBus) pkgconfig(Qt5Script) pkgconfig(Qt5Sql)
BuildRequires: appstream-glib

Requires: dbus-python
Requires: gettext
# odf2xliff
Requires: translate-toolkit
Recommends: poxml
Recommends: subversion

Conflicts: kdesdk-common < 4.10.80
Obsoletes: kdesdk-lokalize < 4.10.80
Provides:  kdesdk-lokalize = %{version}-%{release}

%description
Computer-aided translation system focusing on productivity and performance

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# Add Comment key to .desktop file
grep '^Comment=' %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop || \
desktop-file-install \
  --dir=%{buildroot}%{_kf5_datadir}/applications \
  --set-comment="%{summary}" \
  %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop


%check
#appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop ||:


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%files
%doc COPYING*
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_kf5_datadir}/icons/hicolor/*/apps/%{name}.*
%{_kf5_datadir}/%{name}/
%{_kf5_docdir}/HTML/en/%{name}/
%{_kf5_datadir}/kxmlgui5/%{name}/
%{_kf5_datadir}/config.kcfg/%{name}.kcfg


%changelog
* Fri Dec 18 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-3
- Fix open segfault

* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-5
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- tune desktop file, remove submenu.
- add translate-toolkit require.
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2
