Name: kaccounts-providers
Version: 15.12.0
Release: 2%{?dist}
Summary: Additional service providers for KAccounts framework
License: GPLv2
URL: https://projects.kde.org/projects/kde/kdenetwork/kaccounts-providers

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  kf5-rpm-macros

BuildRequires:  kaccounts-integration-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kpackage-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  intltool
BuildRequires:  libaccounts-glib-devel

Requires:       signon-ui

%description
%{summary}.

%prep
%setup -q -n kaccounts-providers-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%license COPYING
%config %{_sysconfdir}/signon-ui/webkit-options.d/*
%{_kf5_qtplugindir}/kaccounts/ui/owncloud_plugin_kaccounts.so
%dir %{_kf5_datadir}/kpackage/genericqml/org.kde.kaccounts.owncloud
%{_kf5_datadir}/kpackage/genericqml/org.kde.kaccounts.owncloud/*
%{_kf5_datadir}/accounts/providers/google.provider
%{_kf5_datadir}/accounts/providers/owncloud.provider



%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.04.3-2
- Rebuild

