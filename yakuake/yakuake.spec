Name: yakuake
Version: 2.9.9
Release: 14.git
Summary: A drop-down terminal emulator

License: GPLv2 or GPLv3
URL: http://yakuake.kde.org
#git clone git://anongit.kde.org/yakuake
Source0: yakuake.tar.gz

Source1: yakuake-zh_CN.po


Patch0: yakuake-do-not-usewmassist.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-attica-devel
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kauth-devel
BuildRequires: kf5-kcodecs-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kcrash-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kglobalaccel-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-sonnet-devel
BuildRequires: libX11-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtx11extras-devel

Requires: konsole5-part

BuildRequires: desktop-file-utils
BuildRequires: appstream-glib

%description
Yakuake is a drop-down terminal emulator.

%prep
%autosetup -n yakuake -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/yakuake.mo

%find_lang yakuake

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


%files -f yakuake.lang
%doc AUTHORS COPYING ChangeLog TODO
%{_sysconfdir}/xdg/yakuake.knsrc
%{_kf5_bindir}/yakuake
%{_kf5_datadir}/applications/org.kde.yakuake.desktop
%{_kf5_datadir}/icons/hicolor/*/app/%{name}.*
%{_kf5_datadir}/knotifications5/yakuake.notifyrc
%dir %{_kf5_datadir}/yakuake
%{_kf5_datadir}/yakuake/*

%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 2.9.9-14.git
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.9.9-13.git
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- update to latest git.
