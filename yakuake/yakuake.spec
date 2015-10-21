Name:           yakuake
Version:        2.9.9
Release:        10
Summary:        A drop-down terminal emulator

License:	GPLv2 or GPLv3
URL:		http://yakuake.kde.org/
Source0:    yakuake.tar.gz

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: pkgconfig(Qt5Widgets)

Requires:   konsole5-part

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
Yakuake is a drop-down terminal emulator.

%prep
%autosetup -n yakuake

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
%doc AUTHORS COPYING ChangeLog TODO
%{_sysconfdir}/xdg/yakuake.knsrc
%{_kf5_bindir}/yakuake
%{_kf5_datadir}/applications/org.kde.yakuake.desktop
%{_kf5_datadir}/icons/hicolor/*/app/%{name}.*
%{_kf5_datadir}/knotifications5/yakuake.notifyrc
%dir %{_kf5_datadir}/yakuake
%{_kf5_datadir}/yakuake/*

%changelog
