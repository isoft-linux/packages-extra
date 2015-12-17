Name: kdenlive 
Version: 15.12.0
Release: 2 
Summary: Video editing application

License: GPL
URL: http://www.kde.org
Source0: %{name}-%{version}.tar.xz
Patch0: use-bomi-instead-xine.patch

BuildRequires: mlt-devel
BuildRequires: libv4l-devel
BuildRequires: cmake
BuildRequires: pkgconfig gettext python
BuildRequires: extra-cmake-modules
BuildRequires: kf5-rpm-macros
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtscript-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: shared-mime-info
BuildRequires: pkgconfig(gl), pkgconfig(glu)
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kbookmarks-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kplotting-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kdoctools-devel

Requires: shared-mime-info
Requires: dvgrab dvdauthor ffmpeg

%description
Kdenlive is a video editing application, based on MLT Framework and KDE Frameworks 5

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} \
    -Wno-dev \
    -DCMAKE_BUILD_TYPE=Release \
    ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
touch --no-create %{_kf5_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kf5_datadir}/mime ||:

%posttrans
gtk-update-icon-cache %{_kf5_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
update-mime-database -n %{_kf5_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
touch --no-create %{_kf5_datadir}/mime ||:
update-mime-database -n %{_kf5_datadir}/mime &> /dev/null || :
fi

%files
%{_sysconfdir}/xdg/kdenlive_*
%{_kf5_bindir}/kdenlive
%{_kf5_bindir}/kdenlive_render
%{_qt5_plugindir}/mltpreview.so
%{_kf5_datadir}/appdata/kdenlive.appdata.xml
%{_kf5_datadir}/applications/org.kde.kdenlive.desktop
%{_kf5_datadir}/config.kcfg/kdenlivesettings.kcfg

%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/kdenlive

%{_kf5_datadir}/knotifications5/kdenlive.notifyrc
%{_kf5_datadir}/kservices5/mltpreview.desktop
%dir %{_kf5_datadir}/kxmlgui5/kdenlive
%{_kf5_datadir}/kxmlgui5/kdenlive/kdenliveui.rc

%{_datadir}/menu/kdenlive
%{_datadir}/mime/packages/kdenlive.xml
%{_datadir}/mime/packages/westley.xml
%{_datadir}/pixmaps/kdenlive.png

%{_docdir}/HTML/en/kdenlive
%{_mandir}/man1/kdenlive.1.gz
%{_mandir}/man1/kdenlive_render.1.gz

%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-2
- Initial build

