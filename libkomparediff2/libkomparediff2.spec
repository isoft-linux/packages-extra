# enable tests
%global tests 1

Name:    libkomparediff2
Summary: Library to compare files and strings
Version: 15.08.2
Release: 2%{?dist}

# Library: GPLv2+ (some files LGPLv2+), CMake scripts: BSD
License: GPLv2+ and BSD
URL:     https://projects.kde.org/projects/kde/kdesdk/libkomparediff2
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel

Requires:       diffutils

Obsoletes: kompare-libs < 4.11.80
Obsoletes: kdesdk-kompare-libs < 4.10.80

%description
A shared library to compare files and strings using KDE Frameworks 5 and GNU
diff, used in Kompare and KDevelop.

%package devel
Summary: Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake
Requires: qt5-qtbase-devel
Requires: kf5-kcodecs-devel
Requires: kf5-kcoreaddons-devel
Requires: kf5-ki18n-devel
Requires: kf5-kio-devel
Requires: kf5-kxmlgui-devel
# Conflict with old Kompare builds which included libkomparediff2.
Conflicts:      kompare-devel < 4.11.80
# The library was unversioned in 4.10, so conflict with main Kompare package.
Conflicts:      kdesdk-kompare < 4.10.80
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} -DBUILD_TESTING:BOOL=%{?tests}%{!?tests:0} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
%if 0%{?tests}
make test/fast -C %{_target_platform}
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING*
%{_libdir}/libkomparediff2.so.5*

%files devel
%{_includedir}/libkomparediff2/
%{_libdir}/libkomparediff2.so
%{_libdir}/cmake/LibKompareDiff2/


%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-2
- Update

