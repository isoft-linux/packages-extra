Name: krfb
Version: 4.13.0
Release: 5
License: GPL

Source0: krfb-4.13.0.tar.xz 

Patch0: desktop.patch

BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: kf5-kbookmarks-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdnssd-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-kwallet-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-rpm-macros
BuildRequires: freerdp-devel
BuildRequires: libvncserver-devel
BuildRequires: qt5-qtx11extras-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kcrash-devel
BuildRequires: libXtst-devel

Requires: libvncserver libXdamage 

Summary:Desktop Sharing

%description

%prep
%autosetup -n %{name} -p1

%build 
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd
make %{?_smp_mflags} -C %{_target_platform}



%install
make install DESTDIR=%{buildroot} -C %{_target_platform}
#echo "NoDisplay=true" >> $RPM_BUILD_ROOT/usr/share/applications/org.kde.krfb.desktop

%files 
%{_bindir}/krfb
%{_libdir}/libkrfbprivate.so.5
%{_libdir}/libkrfbprivate.so.5.0
%{_libdir}/qt5/plugins/krfb/krfb_framebuffer_qt.so
%{_libdir}/qt5/plugins/krfb/krfb_framebuffer_x11.so
%{_datadir}/applications/org.kde.krfb.desktop
%{_defaultdocdir}/HTML/en/krfb/configuration_network.png
%{_defaultdocdir}/HTML/en/krfb/configuration_security.png
%{_defaultdocdir}/HTML/en/krfb/connection.png
%{_defaultdocdir}/HTML/en/krfb/email_invitation.png
%{_defaultdocdir}/HTML/en/krfb/index.cache.bz2
%{_defaultdocdir}/HTML/en/krfb/index.docbook
%{_defaultdocdir}/HTML/en/krfb/personal_invitation.png
%{_defaultdocdir}/HTML/en/krfb/screenshot.png
%{_datadir}/krfb/krfb.notifyrc
%{_datadir}/kservicetypes5/krfb-framebuffer.desktop


%changelog
* Mon Dec 05 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 4.13.0-5
- Change Exec for desktop.

* Wed Nov 30 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 4.13.0-4
- QA want to display krfb in the category of Internet.

* Thu Dec 10 2015 kun.li@i-soft.com.cn - 4.13.0-3
- rebuilt

