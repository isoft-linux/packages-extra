%define snap 20150703
%define webkit 1

Name:    k3b
Summary: CD/DVD/Blu-ray burning application
Epoch:   1
Version: 2.10.0
Release: 3%{?dist}

License: GPLv2+
URL:     http://www.k3b.org/
%if 0%{?snap:1}
#git clone git://anongit.kde.org/k3b
#git checkout kf5
Source0: k3b-%{version}.tar.bz2
%else
Source0: http://download.kde.org/stable/k3b/k3b-%{version}.tar.xz
%endif

BuildRequires: gettext
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
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kfilemetadata-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: qt5-qtwebkit-devel

BuildRequires: kf5-libkcddb-devel
BuildRequires: libmpcdec-devel
BuildRequires: pkgconfig(dvdread)
BuildRequires: pkgconfig(flac++)
BuildRequires: pkgconfig(libmusicbrainz)
BuildRequires: pkgconfig(samplerate)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(taglib)
BuildRequires: pkgconfig(vorbisenc) pkgconfig(vorbisfile)
BuildRequires: pkgconfig(taglib)

Requires: cdrdao
Requires: dvd+rw-tools
Requires: cdrkit

%description
K3b provides a comfortable user interface to perform most CD/DVD
burning tasks. While the experienced user can take influence in all
steps of the burning process the beginner may find comfort in the
automatic settings and the reasonable k3b defaults which allow a quick
start.

%package common
Summary:  Common files of %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch
%description common
{summary}.

%package libs
Summary: Runtime libraries for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
%description libs
%{summary}.

%package devel
Summary: Files for the development of applications which will use %{name} 
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}

#install -p -m644 %{SOURCE51} src/k3b.appdata.xml

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%{cmake_kf5} \
  -DK3B_BUILD_K3BSETUP:BOOL=OFF \
  -DK3B_BUILD_FFMPEG_DECODER_PLUGIN:BOOL=ON \
  -DK3B_BUILD_LAME_ENCODER_PLUGIN:BOOL=OFF \
  -DK3B_BUILD_MAD_DECODER_PLUGIN:BOOL=ON \
  -DK3B_ENABLE_HAL_SUPPORT:BOOL=OFF \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.k3b.desktop


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
touch --no-create %{_kf5_datadir}/mime ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/iconshicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
touch --no-create %{_kf5_datadir}/mime ||:
update-mime-database %{_kf5_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
update-mime-database %{_kf5_datadir}/mime &> /dev/null || :

%files
%{_kf5_bindir}/k3b
%{_kf5_qtplugindir}/*.so

%{_kf5_datadir}/konqsidebartng/virtual_folders/services/*.desktop
%{_kf5_datadir}/solid/actions/k3b*.desktop
%{_kf5_datadir}/applications/org.kde.k3b.desktop
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/ServiceMenus/*.desktop
%{_kf5_datadir}/kservicetypes5/k3bplugin.desktop

%{_kf5_datadir}/mime/packages/x-k3b.xml
%{_kf5_datadir}/icons/hicolor/*/*/*

%{_kf5_docdir}/HTML/*/k3b/

%files common
%{_kf5_datadir}/k3b/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libk3bdevice.so.*
%{_kf5_libdir}/libk3blib.so.*

%files devel
%{_includedir}/*.h
%{_kf5_libdir}/libk3bdevice.so
%{_kf5_libdir}/libk3blib.so


%changelog
* Mon Nov 28 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 2.10.0-3
- Rebuild for kf5-libkcddb-16.11.80-1
- Rebuild for clang analyzer and sanitizer.

* Thu Jul 21 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 2.10.0-2
- Rebuild for kf5-libkcddb

* Tue Jul 19 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 2.10.0-1
- 2.10.0

* Wed Jul 06 2016 sulit <sulitsrc@gmail.com> - 2:2.9.90-10.git
- epoch add 1 for k3b

* Wed Jul 06 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1:2.9.90-9.git
- Update patch.

* Tue Jul 05 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1:2.9.90-8.git
- Fix QUrl::fromLocalFile and QString filename convert issue.
- add some BuildRequires

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 1:2.9.90-7.git
- Rebuild

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1:2.9.90-6.git
- Rebuild




