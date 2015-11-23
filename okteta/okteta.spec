Name:    okteta
Summary: Binary/hex editor
Version: 15.11.80
Release: 2%{?dist}

License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdesdk/okteta
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kbookmarks-devel
BuildRequires: kf5-kcodecs-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: pkgconfig(qca2-qt5)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5PrintSupport)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5ScriptTools)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: appstream-glib

Conflicts:      kdesdk-common < 4.10.80
Obsoletes:      kdesdk-okteta < 4.10.80
Provides:       kdesdk-okteta = %{version}-%{release}

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Recommends: gccxml libxslt

%description
Okteta is a binary/hex editor for KDE

%package libs
Summary: Runtime libraries and kpart plugins for %{name}
Obsoletes: kdesdk-okteta-libs < 4.10.80
Provides:  kdesdk-okteta-libs = %{version}-%{release}
Provides:  okteta5-part = %{version}-%{release}
Provides:  okteta5-part%{?_isa} = %{version}-%{release}
%description libs
%{summary}.

%package devel
Summary: Developer files for %{name}
Obsoletes: kdesdk-okteta-devel < 4.10.80
Provides:  kdesdk-okteta-devel = %{version}-%{release}
Provides:  okteta5-devel = %{version}-%{release}
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


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

test -f %{buildroot}%{_datadir}/appdata/okteta.appdata.xml &&
mv %{buildroot}%{_datadir}/appdata/okteta.appdata.xml \
   %{buildroot}%{_datadir}/appdata/org.kde.okteta.appdata.xml


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/org.kde.okteta.appdata.xml ||:
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.okteta.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
touch --no-create %{_kde4_datadir}/mime ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-mime-database %{?fedora:-n} %{_kde4_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
touch --no-create %{_datadir}/mime ||:
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%files
%doc COPYING* README
%{_bindir}/okteta
%{_bindir}/struct2osd
%{_datadir}/mime/packages/okteta.xml
%{_datadir}/appdata/org.kde.okteta.appdata.xml
%{_datadir}/applications/org.kde.okteta.desktop
%{_datadir}/kxmlgui5/okteta/
%{_datadir}/icons/hicolor/*/apps/okteta.*
%{_docdir}/HTML/en/okteta/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%dir %{_datadir}/okteta/
%{_datadir}/okteta/structures/
%{_sysconfdir}/xdg/okteta-structures.knsrc
%{_datadir}/config.kcfg/structviewpreferences.kcfg
%{_libdir}/libkasten*.so.*
%{_libdir}/libokteta*.so.*
%{_qt5_plugindir}/designer/oktetadesignerplugin.so

%{_datadir}/kxmlgui5/oktetapart

%{_qt5_plugindir}/oktetapart.so

%files devel
%{_includedir}/Okteta/
%{_includedir}/okteta/
%{_libdir}/libokteta*.so
%{_includedir}/Kasten/
%{_includedir}/kasten/
%{_libdir}/libkasten*.so
%{_libdir}/cmake/KastenControllers/
%{_libdir}/cmake/KastenCore/
%{_libdir}/cmake/KastenGui/
%{_libdir}/cmake/OktetaCore/
%{_libdir}/cmake/OktetaGui/
%{_libdir}/cmake/OktetaKastenControllers/
%{_libdir}/cmake/OktetaKastenCore/
%{_libdir}/cmake/OktetaKastenGui


%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-4
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Update to 15.08.2
