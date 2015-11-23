Name:           kdebugsettings
Summary:        Configure debug output from Qt5 applications
Version:        15.11.80
Release:        2%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/projects/kde/kdeutils/kdebugsettings

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kio-devel

BuildRequires:  desktop-file-utils


Requires:       kf5-filesystem

%description
An application to enable/disable qCDebug

%prep
%setup -q -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
desktop-file-validate %{buildroot}/%{_kf5_datadir}/applications/org.kde.%{name}.desktop

%files
%license COPYING
%{_kf5_bindir}/kdebugsettings
%config %{_sysconfdir}/xdg/kde.categories
%{_kf5_datadir}/applications/org.kde.kdebugsettings.desktop

%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Initial build

