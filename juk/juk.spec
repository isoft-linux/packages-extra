%global tunepimp 0 

Name:    juk 
Summary: Music player 
Version: 15.08.3
Release: 2%{?dist}

# code: KDE e.V. may determine that future GPL versions are accepted
# handbook doc: GFDL
License: (GPLv2 or GPLv3) and GFDL
URL:     https://projects.kde.org/projects/kde/kdemultimedia/%{name}
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz
Patch0: juk-fix-cmake-error.patch

BuildRequires: desktop-file-utils
BuildRequires: kdelibs-devel >= 4.14
BuildRequires: taglib-devel
BuildRequires: appstream-glib

%if 0%{?tunepimp}
BuildRequires: libtunepimp-devel
%endif
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(taglib)

%{?kde_runtime_requires}

# when split occurred
Obsoletes: kdemultimedia-juk < 6:4.8.80
Provides:  kdemultimedia-juk = 6:%{version}-%{release}


%description
Juk is a jukebox, tagger and music collection manager.


%prep
%setup
%patch0 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde --all-name


%check
appstream-util validate-relax --nonet %{buildroot}%{_kde4_datadir}/appdata/%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/juk.desktop


%post 
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans 
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun 
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%files -f %{name}.lang
%doc COPYING HACKING TODO
%{_kde4_appsdir}/juk/
%{_kde4_bindir}/juk
%{_datadir}/dbus-1/interfaces/org.kde.juk.*.xml
%{_kde4_datadir}/kde4/services/ServiceMenus/jukservicemenu.desktop
%{_kde4_datadir}/appdata/%{name}.appdata.xml
%{_kde4_datadir}/applications/kde4/juk.desktop
%{_kde4_iconsdir}/hicolor/*/apps/juk.*


%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2
