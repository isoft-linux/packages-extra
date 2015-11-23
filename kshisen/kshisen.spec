Name:    kshisen
Summary: Shisen-Sho Mahjongg-like tile game
Version: 15.11.80
Release: 2%{?dist}

License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdegames/%{name}
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz
Patch0: kshisen-clean-desktop.patch

BuildRequires: desktop-file-utils
BuildRequires: kf5-rpm-macros
BuildRequires: extra-cmake-modules
BuildRequires: qt5-qtbase-devel

BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kdnssd-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-kdoctools-devel

BuildRequires: phonon-qt5-devel

BuildRequires: libkdegames-devel >= %{version}
BuildRequires: libkmahjongg-devel >= %{version}

%description
Shisen-Sho is a solitaire-like game played using the standard set of Mahjong
tiles. Unlike Mahjong however, Shisen-Sho has only one layer of scrambled tiles.
You can remove matching pieces if they can be connected with a line with at most
two bends in it. At the same time, the line must not cross any other tiles.
To win a game of Shisen-Sho the player has to remove all the tiles from the
game board


%prep
%setup -q
%patch0 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop


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
%license COPYING*
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_kf5_datadir}/sounds/%{name}
%{_kf5_datadir}/config.kcfg/%{name}.kcfg
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/kxmlgui5/kshisen/
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/doc/HTML/en/kshisen/
%{_kf5_datadir}/appdata/org.kde.kshisen.appdata.xml

%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Initial build

