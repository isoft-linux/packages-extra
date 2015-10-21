#global svn_date 20130815

Name:           kde-partitionmanager
Version:        1.2.1
Release:        6%{?dist}
Summary:        KDE Partition Manager

License:        GPLv3+
URL:            http://www.kde.org/applications/system/kdepartitionmanager/
%if 0%{?svn_date}
Source0:        %{name}-%{version}-%{svn_date}svn.tar.xz
%else
Source0:        http://download.kde.org/stable/partitionmanager/%{version}/src/partitionmanager-%{version}.tar.xz
%endif
# probably better to use https://projects.kde.org/projects/playground/sdk/releaseme
# now that it is in kde git infrastructure
Source1:        kdepm-generate-tarball.sh
# Source built using the following commands : sh kdepm-generate-tarball.sh 20130815

#Patch to fix config file name, upstream KDE bug 345857
Patch0:		partitionmanager_config.patch

BuildRequires:  parted-devel, libblkid-devel, libatasmart-devel, gettext, cmake, desktop-file-utils
BuildRequires:	kf5-rpm-macros, kf5-kconfig-devel, kf5-kcrash-devel, kf5-ki18n-devel, kf5-kio-devel, kf5-kdoctools-devel, kf5-kiconthemes-devel, kf5-kwindowsystem-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	extra-cmake-modules

Requires:       parted, e2fsprogs
Requires:	kf5-filesystem

%description
KDE Partition Manager is a utility program to help you manage the disk devices,
partitions and file systems on your computer. It allows you to easily create, 
copy, move, delete, resize without losing data, backup and restore partitions.
 
KDE Partition Manager supports a large number of file systems, 
including ext2/3/4, reiserfs, NTFS, FAT16/32, jfs, xfs and more.
 
It makes use of external programs to get its job done, so you might have to 
install additional software (preferably packages from your distribution) 
to make use of all features and get full support for all file systems.


%prep
%setup -q -n partitionmanager-%{version}

%patch0 -p1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}
%find_lang partitionmanager --with-kde

# Validate .desktop file
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/*PartitionManager.desktop


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f partitionmanager.lang
%doc README CHANGES
%license COPYING.GPL3
%{_kf5_bindir}/partitionmanager
%{_kf5_libdir}/libpartitionmanager*.so
%{_kf5_qtplugindir}/libpm*.so
%{_kf5_datadir}/applications/*PartitionManager.desktop
%{_kf5_datadir}/kservices5/pm*backendplugin.desktop
%{_kf5_datadir}/kservicetypes5/pm*backendplugin.desktop
%{_kf5_datadir}/partitionmanager/
%{_kf5_datadir}/config.kcfg/partitionmanager.kcfg
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/appdata/*PartitionManager.appdata.xml
%{_docdir}/HTML/*/partitionmanager/*

%changelog
