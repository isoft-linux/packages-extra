Name:    gwenview 
Summary: An image viewer
Version: 15.08.2
Release: 4 

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/gwenview

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif 
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

## upstreamable patches

BuildRequires: cmake 
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kactivities-devel
buildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-kio-devel
## frameworks soon to come (hopefully) -- rex
#BuildRequires: kf5-kdcraw-devel
#BuildRequires: kf5-kipi-devel
BuildRequires: appstream-glib
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Widgets) pkgconfig(Qt5Script) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Concurrent) pkgconfig(Qt5Svg) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5X11Extras)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# when split occurred
Conflicts: kdegraphics < 7:4.6.95-10

%description
%{summary}.

%package  libs 
Summary:  Runtime files for %{name} 
# wrt (LGPLv2 or LGPLv3), KDE e.V. may determine that future GPL versions are accepted 
License:  IJG and LGPLv2+ and GPLv2+ and LGPLv2 or LGPLv3
%description libs 
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


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/org.kde.%{name}.desktop


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files 
%doc COPYING 
%{_kf5_bindir}/%{name}*
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_docdir}/HTML/en/gwenview/
%{_kf5_datadir}/kservices5/gvpart.desktop
%{_kf5_datadir}/gwenview/
%{_kf5_datadir}/kservices5/ServiceMenus/slideshow.desktop
%{_kf5_datadir}/kxmlgui5/org.kde.gwenview
%{_kf5_datadir}/kxmlgui5/gvpart/gvpart.rc

%files libs
%{_kf5_libdir}/libgwenviewlib.so.*
%{_kf5_qtplugindir}/gvpart.so


%changelog
* Thu Oct 15 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2

