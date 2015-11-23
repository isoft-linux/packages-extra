Name:    kcachegrind
Summary: GUI to profilers such as Valgrind
Version: 15.11.80
Release: 2

License: GPLv2 and GFDL
URL:     https://projects.kde.org/projects/kde/kdesdk/kcachegrind
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils

BuildRequires:  cmake
#for kde4 rpm macros.
BuildRequires:  kde-filesystem
BuildRequires:  kdelibs-devel >= 4.14

Requires: desktop-file-utils
Requires: shared-mime-info

Conflicts:      kdesdk-common < 4.10.80
Provides:       kdesdk-kcachegrind = %{version}-%{release}
Obsoletes:      kdesdk-kcachegrind < 4.10.80

%description
Browser for data produced by profiling tools (e.g. cachegrind)

%prep
%setup -q -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang kcachegrind --with-kde --without-mo

%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/%{name}.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:


%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime >& /dev/null ||:


%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime >& /dev/null ||:
fi


%files -f kcachegrind.lang
%doc README COPYING COPYING.DOC
%{_kde4_bindir}/kcachegrind
%{_kde4_bindir}/dprof2calltree
%{_kde4_bindir}/hotshot2calltree
%{_kde4_bindir}/memprof2calltree
%{_kde4_bindir}/op2calltree
%{_kde4_bindir}/pprof2calltree
%{_kde4_appsdir}/kcachegrind/
%{_kde4_datadir}/applications/kde4/kcachegrind.desktop
%{_kde4_iconsdir}/hicolor/*/apps/kcachegrind.*

%changelog
* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2

