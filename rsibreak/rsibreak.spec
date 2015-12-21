Name: rsibreak
Summary: A small utility which bothers you at certain intervals
Version: 0.12
Release: 2.git%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/unmaintained/rsibreak
# git://anongit.kde.org/rsibreak.git
Source0: rsibreak.tar.gz
#po for zh_CN
Source1: rsibreak-zh_CN.po

#sounds token from workrave and enc to ogg.
Source2: sounds.tar.gz

Patch0: fix-segfault.patch
Patch1: rsibreak-various-zh-CN-fix.patch
Patch2: rsibreak-add-sounds.patch
Patch3: rsibreak-setup-dialog-minimum-size.patch
Patch4: rsibreak-fix-tray-menu.patch
#plasma dash board almost useless
Patch5: rsibreak-remove-show-plasma-dashboard.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: qt5-qtbase-devel qt5-qttools-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kidletime-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kwindowsystem-devel

%description
RSIBreak is a small utility which bothers you at certain intervals. The
interval and duration of two different timers can be configured. You can
use the breaks to stretch out or do the dishes. The aim of this utility
is to let you know when it is time to have a break from your computer.
This can help people to prevent Repetive Strain Injury.


%prep
%setup -q -n %{name} -a2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES
msgfmt %{SOURCE1} -o %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/rsibreak.mo

%find_lang %{name} --with-kde

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*rsibreak.desktop

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS TODO
%{_sysconfdir}/xdg/autostart/*.desktop
%{_kf5_bindir}/rsibreak
%{_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/knotifications5/rsibreak.notifyrc
%{_datadir}/dbus-1/interfaces/org.rsibreak.rsiwidget.xml
%{_datadir}/applications/*.desktop
%dir %{_datadir}/sounds/rsibreak
%{_datadir}/sounds/rsibreak/*

%changelog
* Sat Dec 19 2015 Cjacker <cjacker@foxmail.com> - 0.12-2.git
- Update to 0.12 kf5 version

* Fri Dec 18 2015 Cjacker <cjacker@foxmail.com> - 0.11-3
- Add updated zh_CN po

* Fri Dec 18 2015 Cjacker <cjacker@foxmail.com> - 0.11-2
- Update

