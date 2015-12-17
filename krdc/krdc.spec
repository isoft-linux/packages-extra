Name: krdc
Version: 15.08.0 
Release: 3
License: GPL

Source0: krdc-15.08.0.tar.xz  
Patch0: disable-doc.patch
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

Requires: libvncserver freerdp
Requires: kf5-kcmutils kf5-kdnssd kf5-knotifyconfig libvncserver 

Summary:Remote Desktop Client
Provides: kdenetwork-krdc 

%description
Remote Desktop Client

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

%files
%{_bindir}/krdc
%{_includedir}/krdc/hostpreferences.h
%{_includedir}/krdc/remoteview.h
%{_includedir}/krdc/remoteviewfactory.h
%{_includedir}/krdccore_export.h
%{_libdir}/libkrdccore.so
%{_libdir}/libkrdccore.so.15.12.0
%{_libdir}/libkrdccore.so.5
%{_libdir}/qt5/plugins/krdc/kcms/libkcm_krdc_vncplugin.so
%{_libdir}/qt5/plugins/krdc/libkrdc_testplugin.so
%{_libdir}/qt5/plugins/krdc/libkrdc_vncplugin.so
%{_datadir}/applications/org.kde.krdc.desktop
%{_datadir}/config.kcfg/krdc.kcfg
%{_datadir}/krdc/pics/pointcursor.png
%{_datadir}/krdc/pics/pointcursormask.png
%{_datadir}/kservices5/krdc_vnc_config.desktop
%{_datadir}/kservices5/vnc.protocol
%{_datadir}/kxmlgui5/krdc/krdcui.rc

%changelog
* Thu Dec 10 2015 kun.li@i-soft.com.cn - 15.08.0-3
- rebuilt
