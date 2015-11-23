Name:    kcron
Summary: Cron KDE configuration module
Version: 15.11.80
Release: 2%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdeadmin/kcron
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: appstream-glib
BuildRequires: extra-cmake-modules
BuildRequires: kf5-rpm-macros

BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kxmlgui-devel

BuildRequires: pkgconfig(Qt5Widgets) pkgconfig(Qt5PrintSupport)

Conflicts:      kdeadmin < 4.10.80
Obsoletes:      kdeadmin < 4.10.80

%description
Systemsettings module for the cron task scheduler.

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
#appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/%{name}.appdata.xml ||:
#desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop ||:


%files
%{_kf5_docdir}/HTML/en/%{name}/
%{_kf5_qtplugindir}/kcm_cron.so
%{_kf5_datadir}/kservices5/kcm_cron.desktop


%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2

