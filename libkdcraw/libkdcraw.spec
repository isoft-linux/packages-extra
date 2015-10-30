%global _kde4_build_tests -DKDE4_BUILD_TESTS:BOOL=ON
Name:    libkdcraw
Summary: A C++ interface around LibRaw library
Version: 15.08.1
Release: 3%{?dist}

# libkdcraw is GPLv2+,
# LibRaw(bundled) is LGPLv2
# demosaic-pack GPLv2+ GPLv3+ (addons to libraw)
License: GPLv2+ and LGPLv2 and GPLv3+
URL:     https://projects.kde.org/projects/kde/kdegraphics/libs/libkdcraw
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz
Patch0: libkdcraw-fix-cmake-error.patch

## upstream patches

BuildRequires: kdelibs4-devel
BuildRequires: pkgconfig(libraw) >= 0.15

%{?kdelibs4_requires}

# when split occurred
Conflicts: kdegraphics-libs < 7:4.6.95-10

%description
Libkdcraw is a C++ interface around LibRaw library used to decode RAW
picture files. More information about LibRaw can be found at
http://www.libraw.org.

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel 
%description devel
%{summary}.


%prep
%setup -q
%patch0 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
pkg-config --modversion libkdcraw
make -C %{_target_platform}/tests


%post
/sbin/ldconfig
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_kde4_libdir}/libkdcraw.so.23*
%{_kde4_appsdir}/libkdcraw/
%{_kde4_iconsdir}/hicolor/*/*/*

%files devel
%{_kde4_libdir}/libkdcraw.so
%{_kde4_libdir}/pkgconfig/libkdcraw.pc
%{_kde4_includedir}/libkdcraw/


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.1-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 15.08.1-2
- Initial build.


