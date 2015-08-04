Name:    kf5-purpose
Summary: Provides an abstraction to provide and leverage actions of a specific kind
Version: 5.0.0
Release: 3.git%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/libs/libkexiv2
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

#git clone git://anongit.kde.org/purpose
#git checkout frameworks 
Source0: purpose.tar.gz

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

BuildRequires: kaccounts-integration-devel
%description
Purpose offers the possibility to create integrate services and actions on
any application without having to implement them specifically. Purpose will
offer them mechanisms to list the different alternatives to execute given the
requested action type and will facilitate components so that all the plugins
can receive all the information they need.

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.


%prep
%autosetup -n purpose

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check


%post
/sbin/ldconfig
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi


%files
%{_kf5_libdir}/libKF5Purpose.so.*
%{_kf5_libdir}/libKF5PurposeWidgets.so.*
%{_kf5_libdir}/libReviewboardHelpers.so
%{_kf5_qtplugindir}/purpose/

%{_kf5_datadir}/purpose/
%{_kf5_datadir}/accounts/services/google-youtube.service
%{_kf5_datadir}/icons/hicolor/*/*/*

%{_kf5_qmldir}/org/kde/purpose/

%files devel
%{_libdir}/cmake/KDEExperimentalPurpose/
%{_kf5_libdir}/libKF5PurposeWidgets.so
%{_kf5_libdir}/libKF5Purpose.so
%{_kf5_includedir}/purposewidgets/
%{_kf5_includedir}/purpose/
