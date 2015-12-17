Name:    kompare
Summary: Diff tool
Version: 15.12.0
Release: 2%{?dist}

License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdesdk/kompare
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
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-ktexteditor-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  libkomparediff2-devel >= %{version}
BuildRequires:  desktop-file-utils

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Conflicts:      kdesdk-common < 4.10.80
Obsoletes:      kdesdk-kompare < 4.10.80
Provides:       kdesdk-kompare = %{version}-%{release}
Provides:       mergetool

%description
Tool to visualize changes between two versions of a file

%package libs
Summary: Runtime libraries for %{name}
Obsoletes: kdesdk-kompare-libs < 4.10.80
Provides:  kdesdk-kompare-libs = %{version}-%{release}
Requires:  %{name} = %{version}-%{release}
# help upgrade path since newer libkomparediff2 Obsoletes: kompare-libs < 4.11.80
Requires:  libkomparediff2%{?_isa}
%description libs
This package contains shared libraries for %{name}.

%package devel
Summary: Developer files for %{name}
Obsoletes: kdesdk-kompare-devel < 4.10.80
Provides:  kdesdk-kompare-devel = %{version}-%{release}
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}
Requires:  qt5-qtbase-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.%{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-mime-database %{_datadir}/mime >& /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-mime-database %{_datadir}/mime >& /dev/null ||:
fi

%files
%doc README
%license COPYING COPYING.DOC
%{_bindir}/kompare
%{_datadir}/kxmlgui5/kompare/
%{_datadir}/kservicetypes5/kompare*.desktop
%{_kf5_qtplugindir}/komparenavtreepart.so
%{_kf5_qtplugindir}/komparepart.so
%{_datadir}/applications/org.kde.kompare.desktop
%{_datadir}/icons/hicolor/*/apps/kompare.*
%{_datadir}/kservices5/komparenavtreepart.desktop
%{_datadir}/kservices5/komparepart.desktop
%{_docdir}/HTML/en/kompare/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libkomparedialogpages.so.*
%{_libdir}/libkompareinterface.so.*

%files devel
%{_includedir}/kompare/
%{_libdir}/libkompareinterface.so


%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-2
- Update

