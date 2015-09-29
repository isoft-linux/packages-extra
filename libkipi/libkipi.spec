Name:    libkipi
Summary: Common plugin infrastructure for KDE image applications
Version: 15.07.90
Release: 2

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdegraphics/libs/libkexiv2
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: kdelibs-devel

%{?kdelibs4_requires}

# when split occurred
Conflicts: kdegraphics-libs < 7:4.6.95-10

%description
Kipi (KDE Image Plugin Interface) is an effort to develop a common plugin
structure (for Digikam, Gwenview, etc.). Its aim is to share
image plugins among graphic applications.

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs-devel 
%description devel
%{summary}.


%prep
%setup


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
pkg-config --modversion libkipi


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
%doc AUTHORS COPYING README
%{_kde4_libdir}/libkipi.so.11*
%{_kde4_appsdir}/kipi/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_datadir}/kde4/servicetypes/kipiplugin.desktop

%files devel
%{_kde4_libdir}/libkipi.so
%{_kde4_libdir}/pkgconfig/libkipi.pc
%{_kde4_includedir}/libkipi/


%changelog
