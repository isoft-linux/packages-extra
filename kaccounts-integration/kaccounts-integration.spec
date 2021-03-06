Name: kaccounts-integration
Version: 15.12.0
Release: 2%{?dist}
Summary: Small system to administer web accounts across the KDE desktop
License: GPLv2+
URL: https://projects.kde.org/projects/kde/kdenetwork/kaccounts-integration

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel qt5-qtdeclarative-devel

BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kdeclarative-devel 
BuildRequires:  libaccounts-qt5-devel
BuildRequires:  signon-devel

Requires:       signon
Requires:       signon-plugin-oauth2

Obsoletes:      kaccounts < 15.03
Provides:       kaccounts = %{version}-%{release}

%description
Small system to administer web accounts for the sites and services
across the KDE desktop.

%package        devel
Summary:        Development files for accounts-qt
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
Requires:       kf5-kcoreaddons-devel%{?_isa}
Requires:       libaccounts-qt5-devel%{?_isa}
Requires:       signon-devel%{?_isa}

%description    devel
Headers, development libraries and documentation for %{name}.

%prep
%setup -q -n kaccounts-integration-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%license COPYING
%{_kf5_qtplugindir}/kcm_kaccounts.so
%{_kf5_datadir}/kservices5/kcm_kaccounts.desktop
%{_kf5_qtplugindir}/kded_accounts.so
%{_kf5_datadir}/kservices5/kded/accounts.desktop
%{_kf5_libdir}/libkaccounts.so.*

%{_libdir}/qt5/qml/org/kde/kaccounts/libkaccountsdeclarativeplugin.so
%{_libdir}/qt5/qml/org/kde/kaccounts/qmldir


%files devel
%{_kf5_libdir}/libkaccounts.so
%{_kf5_libdir}/cmake/KAccounts
%{_includedir}/KAccounts

%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.04.3-2
- Rebuild

