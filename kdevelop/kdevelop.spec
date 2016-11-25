%define kdevplatform_ver 5.0.2 

Name:    kdevelop
Summary: Integrated Development Environment for C++/C
Version: 5.0.2
Release: 2%{?dist}

License: GPLv2
URL:     http://www.kdevelop.org/
Source0: http://download.kde.org/stable/kdevelop/%{version}/src/kdevelop-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: qt5-qtbase-devel qt5-qtdeclarative-devel qt5-qtwebkit-devel qt5-qtscript-devel 
BuildRequires: kf5-rpm-macros
BuildRequires: python-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kitemmodels-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-kcmutils-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-krunner-devel
BuildRequires: kf5-plasma-devel
BuildRequires: kf5-kcrash-devel

BuildRequires: libllvm-devel
BuildRequires: libclang-devel
BuildRequires: llvm
BuildRequires: clang
BuildRequires: shared-mime-info
BuildRequires: qt5-qttools-devel

BuildRequires: kdevelop-pg-qt-devel
BuildRequires: kdevplatform-devel >= %{kdevplatform_ver}

Requires: git
Requires: cmake
Requires: clang

%description
The KDevelop Integrated Development Environment provides many features
that developers need as well as providing a unified interface to programs
like gdb, the C/C++ compiler, and make. KDevelop manages or provides:

All development tools needed for C++ programming like Compiler,
Linker, automake and autoconf; KAppWizard, which generates complete,
ready-to-go sample applications; Classgenerator, for creating new
classes and integrating them into the current project; File management
for sources, headers, documentation etc. to be included in the
project; The creation of User-Handbooks written with SGML and the
automatic generation of HTML-output with the KDE look and feel;
Automatic HTML-based API-documentation for your project's classes with
cross-references to the used libraries; Internationalization support
for your application, allowing translators to easily add their target
language to a project;

KDevelop also includes WYSIWYG (What you see is what you get)-creation
of user interfaces with a built-in dialog editor; Debugging your
application by integrating KDbg; Editing of project-specific pixmaps
with KIconEdit; The inclusion of any other program you need for
development by adding it to the "Tools"-menu according to your
individual needs.


%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%setup -q -n kdevelop-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --all-name --with-kde

%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/*.desktop

%post
/sbin/ldconfig
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
touch --no-create %{_kf5_datadir}/mime ||:

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
touch --no-create %{_kf5_datadir}/mime ||:
update-mime-database -n %{_kf5_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
update-mime-database -n %{_kf5_datadir}/mime &> /dev/null || :

%files
%{_kf5_bindir}/kdevelop!
%{_kf5_bindir}/kdev_includepathsconverter
%{_kf5_bindir}/kdevelop
%{_kf5_libdir}/libkdevcmakecommon.so
%{_kf5_libdir}/libKDevClangPrivate.so*
%{_kf5_qtplugindir}/plasma/dataengine/plasma_engine_kdevelopsessions.so
%{_kf5_qtplugindir}/kdevplatform/*/*.so
%{_kf5_qtplugindir}/krunner_kdevelopsessions.so
%{_kf5_datadir}/kdevqmljssupport
%{_kf5_datadir}/kdevmanpage
%{_kf5_datadir}/kdevgdb
%{_kf5_datadir}/appdata/org.kde.kdevelop.appdata.xml
%{_kf5_datadir}/kdevcodegen/templates/*
%{_kf5_datadir}/kdevqmakebuilder
%{_kf5_datadir}/mime/packages/kdevelop.xml
%{_kf5_datadir}/mime/packages/kdevelopinternal.xml
%{_docdir}/HTML/*/kdevelop
%{_kf5_datadir}/plasma/services/org.kde.plasma.dataengine.kdevelopsessions.operations
%{_kf5_datadir}/plasma/plasmoids/kdevelopsessions
%{_kf5_datadir}/kdevappwizard/templates/*
%{_kf5_datadir}/kservices5/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/knotifications5/kdevelop.notifyrc

%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_kf5_datadir}/kdevelop
%{_kf5_datadir}/kdevfiletemplates
%{_datadir}/applications/org.kde.kdevelop.desktop
%{_datadir}/applications/org.kde.kdevelop_ps.desktop

%{_datadir}/locale/*/LC_MESSAGES/*.mo
%dir %{_datadir}/kdevclangsupport
%{_datadir}/kdevclangsupport/*

%files devel
%dir %{_libdir}/cmake/KDevelop
%{_libdir}/cmake/KDevelop/*.cmake
%{_includedir}/kdevelop/

%changelog
* Fri Nov 25 2016 cjacker - 5.0.2-2
- Update to 5.0.2

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 4.90.90-2
- Initial build


