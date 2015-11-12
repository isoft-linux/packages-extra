Name:    kde-dev-scripts
Summary: KDE SDK scripts
Version: 15.08.3
Release: 2%{?dist}

License: GPLv2+ and GPLv2+ and BSD
URL:     https://projects.kde.org/projects/kde/kdesdk/kde-dev-scripts
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

#preset environment variables.
Source1: kde-dev-scripts.sh 

BuildRequires:  desktop-file-utils

#for kde4 rpm macros
BuildRequires:  kde-filesystem

BuildRequires:  kdelibs-devel >= 4.14

# for python macros
BuildRequires:  python-devel
# for env replacement in %%install
BuildRequires:  sed

Requires:       advancecomp
Requires:       optipng

BuildArch:      noarch

Conflicts:      kdesdk-common < 4.10.80
Provides:       kdesdk-scripts = %{version}-%{release}
Obsoletes:      kdesdk-scripts < 4.10.80

%description
KDE SDK scripts


%prep
%setup -q


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
# This one fits better into krazy2 (it requires krazy2), and the version in
# kdesdk does not understand lib64.
rm -f %{buildroot}%{_kde4_bindir}/krazy-licensecheck

#install preset environment variables script.
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/

%files
%doc README COPYING
%{_sysconfdir}/profile.d/*.sh

%{_kde4_bindir}/c++-copy-class-and-file
%{_kde4_bindir}/c++-rename-class-and-file
%{_kde4_bindir}/svnrevertlast
%{_kde4_bindir}/fixuifiles
%{_kde4_bindir}/cvscheck
%{_kde4_bindir}/extend_dmalloc
%{_kde4_bindir}/extractattr
%{_kde4_bindir}/noncvslist
%{_kde4_bindir}/pruneemptydirs
%{_kde4_bindir}/cvsrevertlast
%{_kde4_bindir}/create_makefile
%{_kde4_bindir}/colorsvn
%{_kde4_bindir}/cvslastchange
%{_kde4_bindir}/svngettags
%{_kde4_bindir}/create_svnignore
%{_kde4_bindir}/svnchangesince
%{_kde4_bindir}/build-progress.sh
%{_kde4_bindir}/package_crystalsvg
%{_kde4_bindir}/svnbackport
%{_kde4_bindir}/svnlastlog
%{_kde4_bindir}/cxxmetric
%{_kde4_bindir}/kdemangen.pl
%{_kde4_bindir}/cvsforwardport
%{_kde4_bindir}/includemocs
%{_kde4_bindir}/svnlastchange
%{_kde4_bindir}/wcgrep
%{_kde4_bindir}/qtdoc
%{_kde4_bindir}/nonsvnlist
%{_kde4_bindir}/svnforwardport
%{_kde4_bindir}/create_cvsignore
%{_kde4_bindir}/svnintegrate
%{_kde4_bindir}/kdekillall
%{_kde4_bindir}/create_makefiles
%{_kde4_bindir}/cvsbackport
%{_kde4_bindir}/fixkdeincludes
%{_kde4_bindir}/kde-systemsettings-tree.py
%{_kde4_bindir}/zonetab2pot.py
%{_kde4_bindir}/kde_generate_export_header
%{_kde4_bindir}/cvs-clean
%{_kde4_bindir}/kdelnk2desktop.py
%{_kde4_bindir}/findmissingcrystal
%{_kde4_bindir}/adddebug
%{_kde4_bindir}/cvsversion
%{_kde4_bindir}/cheatmake
%{_kde4_bindir}/cvsblame
%{_kde4_bindir}/optimizegraphics
%{_kde4_bindir}/cvsaddcurrentdir
%{_kde4_bindir}/fix-include.sh
%{_kde4_bindir}/kdedoc
%{_kde4_bindir}/svn-clean
%{_kde4_bindir}/png2mng.pl
%{_kde4_bindir}/extractrc
%{_kde4_bindir}/makeobj
%{_kde4_bindir}/cvslastlog
%{_kde4_bindir}/svnversions
%{_kde4_bindir}/draw_lib_dependencies
%{_kde4_bindir}/reviewboard-am
%{_mandir}/man1/adddebug.1.gz
%{_mandir}/man1/cheatmake.1.gz
%{_mandir}/man1/create_cvsignore.1.gz
%{_mandir}/man1/create_makefile.1.gz
%{_mandir}/man1/create_makefiles.1.gz
%{_mandir}/man1/cvscheck.1.gz
%{_mandir}/man1/cvslastchange.1.gz
%{_mandir}/man1/cvslastlog.1.gz
%{_mandir}/man1/cvsrevertlast.1.gz
%{_mandir}/man1/cxxmetric.1.gz
%{_mandir}/man1/extend_dmalloc.1.gz
%{_mandir}/man1/extractrc.1.gz
%{_mandir}/man1/fixincludes.1.gz
%{_mandir}/man1/pruneemptydirs.1.gz
%{_mandir}/man1/qtdoc.1.gz
%{_mandir}/man1/reportview.1.gz
%{_mandir}/man1/transxx.1.gz
%{_mandir}/man1/zonetab2pot.py.1.gz


%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-2
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- 15.08.2

