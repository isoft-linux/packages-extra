Name:    kapptemplate
Summary: KDE Template generator
Version: 15.11.80
Release: 2%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdesdk/kapptemplate
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
BuildRequires: kf5-rpm-macros
BuildRequires: qt5-qtbase-devel

BuildRequires: appstream-glib-devel

BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kdoctools-devel

Conflicts:      kdesdk-common < 4.10.80
Provides:       kdesdk-kapptemplate = %{version}-%{release}
Obsoletes:      kdesdk-kapptemplate < 4.10.80


%description
Factory for the easy creation of KDE/Qt components and programs

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
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/%{name}.desktop ||:


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-mime-database %{_kf5_datadir}/mime >& /dev/null ||:

fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-mime-database %{_kf5_datadir}/mime >& /dev/null ||:

%files
%doc COPYING*
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/apps/%{name}.*
%{_kf5_datadir}/kdevappwizard/
%{_kf5_docdir}/HTML/en/%{name}/
%{_kf5_datadir}/config.kcfg/%{name}.kcfg


%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2

