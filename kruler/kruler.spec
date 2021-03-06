Name:    kruler
Summary: A screen ruler and color measurement tool 
Version: 15.12.0
Release: 2%{?dist}

License: GPLv2 and GFDL
URL:     https://projects.kde.org/projects/kde/kdegraphics/kruler
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif 

Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: libX11-devel
BuildRequires: libxcb-devel
BuildRequires: pkgconfig(Qt5Widgets) pkgconfig(Qt5X11Extras)

BuildRequires: appstream-glib

# when split occurred
Conflicts: kdegraphics < 7:4.6.95-10

%description
%{summary}.


%prep
%setup -q


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml ||:
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
#doc README
%{_kf5_bindir}/%{name}
#{_sysconfdir}/xdg/%{name}.knsrc
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
#{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/actions/%{name}*
%{_kf5_datadir}/icons/hicolor/*/apps/%{name}.*
%{_kf5_datadir}/%{name}/
%{_kf5_docdir}/HTML/en/%{name}/
#{_kf5_datadir}/kconf_update/%{name}*
%{_kf5_datadir}/knotifications5/%{name}.notifyrc
#{_kf5_datadir}/kxmlgui5/%{name}/
#{_kf5_datadir}/sounds/%{name}/
#{_kf5_datadir}/config.kcfg/%{name}.kcfg


%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2

* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.1
