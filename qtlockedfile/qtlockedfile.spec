%global commit	17b56547d6e0d9a06603231fe2384474f9144829

Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	2.4
Release:	17%{?dist}

License:	GPLv3 or LGPLv2 with exceptions
URL:		http://doc.qt.digia.com/solutions/4/qtlockedfile/qtlockedfile.html
Source0:	https://qt.gitorious.org/qt-solutions/qt-solutions/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz
Source1:	qtlockedfile.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source2:	LICENSE.LGPL
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source3:	LGPL_EXCEPTION
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source4:	LICENSE.GPL3
Patch0:		qtlockedfile-use-current-version.patch
Patch1:		qtlockedfile-dont-build-example.patch

BuildRequires:	qt4-devel qt5-qtbase-devel

%description
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel

%description devel
This package contains libraries and header files for developing applications
that use QtLockedFile.

%package qt5
Summary:	QFile extension with advisory locking functions (Qt5)
Requires:	qt5-qtbase

%description qt5
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.
This is a special build against Qt5.

%package qt5-devel
Summary:	Development files for %{name}-qt5
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	qt5-qtbase-devel

%description qt5-devel
This package contains libraries and header files for developing applications
that use QtLockedFile with Qt5.


%prep
%setup -qnqt-solutions-qt-solutions/%{name}
%patch0
%patch1
sed -i s,head,%{version}, common.pri
mkdir licenses
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} licenses


%build
# Does not use GNU configure
./configure -library
qmake-qt4
make %{?_smp_mflags}
mkdir qt5
pushd qt5
sed -i 's/QtSolutions_LockedFile-2.4/Qt$${QT_MAJOR_VERSION}Solutions_LockedFile-2.4/g' ../common.pri
%{qmake_qt5} ..
make %{?_smp_mflags}
popd

%install
# libraries
mkdir -p %{buildroot}%{_libdir}
cp -a lib/* %{buildroot}%{_libdir}

# headers
for qtdir in %{_qt4_headerdir} %{_qt5_headerdir} ; do
 d=%{buildroot}$qtdir/QtSolutions ;
 mkdir -p $d ;
 cp -a \
    src/qtlockedfile.h \
    src/QtLockedFile \
    $d ;
done

install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt4_datadir}/mkspecs/features/qtlockedfile.prf
install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt5_archdatadir}/mkspecs/features/qtlockedfile.prf


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license licenses/*
%doc README.TXT
# Caution! do not include any unversioned .so symlink (belongs to -devel)
%{_libdir}/libQtSolutions_LockedFile*.so.*

%files devel
%doc doc/html/ example/
%{_qt4_headerdir}/QtSolutions/
%{_libdir}/libQtSolutions_LockedFile*.so
%{_qt4_datadir}/mkspecs/features/qtlockedfile.prf

%files qt5
%license licenses/*
%doc README.TXT
# Caution! do not include any unversioned .so symlink (belongs to -devel)
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so.*

%files qt5-devel
%doc doc/html/ example/
%{_qt5_headerdir}/QtSolutions/
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so
%{_qt5_archdatadir}/mkspecs/features/qtlockedfile.prf


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4-17
- Rebuild

