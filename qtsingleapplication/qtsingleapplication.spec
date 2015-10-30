%global commit 8c2c3f0bde67e64c627c903b718bec92ace28680

Summary:    Qt library to start applications only once per user
Name:       qtsingleapplication
Version:    2.6.1
Release:    18%{?dist}

License:    GPLv3 or LGPLv2 with exceptions
URL:        http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html
Source0:    https://qt.gitorious.org/qt-solutions/qt-solutions/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz
# Proposed upstream in https://codereview.qt-project.org/#/c/92417/
Source1:    qtsingleapplication.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92416/
Source2:    qtsinglecoreapplication.prf
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source3:    LICENSE.GPL3
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source4:    LICENSE.LGPL
# Proposed upstream in https://codereview.qt-project.org/#/c/92411/
Source5:    LGPL_EXCEPTION

# Proposed upstream in https://codereview.qt-project.org/#/c/92416/
Patch0:     qtsingleapplication-build-qtsinglecoreapplication.patch
# Proposed upstream in https://codereview.qt-project.org/#/c/92415/
Patch1:     qtsingleapplication-remove-included-qtlockedfile.patch

Patch2:     qtsingleapplication-fix-build-with-qt-5.5.patch

BuildRequires: qt4-devel qtlockedfile-devel
BuildRequires: qt5-qtbase-devel qtlockedfile-qt5-devel

%description
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   qt4-devel

%description devel
This package contains libraries and header files for developing applications
that use QtSingleApplication.

%package -n qtsinglecoreapplication
Summary:    Qt library to start applications only once per user
Requires:   qt4

%description -n qtsinglecoreapplication
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

%package -n qtsinglecoreapplication-devel
Summary:    Development files for qtsinglecoreapplication
Requires:   qtsinglecoreapplication = %{version}-%{release}
Requires:   qt4-devel

%description -n qtsinglecoreapplication-devel
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.

%package qt5
Summary:    Qt5 library to start applications only once per user
Requires:   qt5-qtbase

%description qt5
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

This is a special build against Qt5.

%package qt5-devel
Summary:    Development files for %{name}-qt5
Requires:   %{name}-qt5 = %{version}-%{release}
Requires:   qt5-qtbase-devel

%description qt5-devel
This package contains libraries and header files for developing applications
that use QtSingleApplication with Qt5.

%package -n qtsinglecoreapplication-qt5
Summary:    Qt library to start applications only once per user (Qt5)
Requires:   qt5-qtbase

%description -n qtsinglecoreapplication-qt5
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

This is a special build against Qt5.

%package -n qtsinglecoreapplication-qt5-devel
Summary:    Development files for qtsinglecoreapplication-qt5
Requires:   qtsinglecoreapplication-qt5 = %{version}-%{release}
Requires:   qt5-qtbase-devel

%description -n qtsinglecoreapplication-qt5-devel
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.


%prep
%setup -qnqt-solutions-qt-solutions/%{name}
%patch0 -p0
%patch1 -p0

mkdir licenses
cp -p %{SOURCE3} %{SOURCE4} %{SOURCE5} licenses

# We already disabled bundling this external library.
# But just to make sure:
rm -rf ../qtlockedfile/
sed -i 's,qtlockedfile\.h,QtSolutions/\0,' src/qtlocalpeer.h
rm src/{QtLocked,qtlocked}*


%build
# Does not use GNU configure
./configure -library
qmake-qt4
make %{?_smp_mflags}

mkdir qt5
cat %{PATCH2}|patch -p1
pushd qt5
sed -i 's/QtSolutions_SingleApplication-2.6/Qt$${QT_MAJOR_VERSION}Solutions_SingleApplication-2.6/g' ../common.pri
sed -i 's/QtSolutions_SingleCoreApplication-2.6/Qt$${QT_MAJOR_VERSION}Solutions_SingleCoreApplication-2.6/g' ../common.pri
qmake-qt5 ..
make %{?_smp_mflags}
popd


%install
# libraries
mkdir -p %{buildroot}%{_libdir}
cp -a lib/* %{buildroot}%{_libdir}
chmod 755 %{buildroot}%{_libdir}/*.so*

# headers
for qtdir in %{_qt4_headerdir} %{_qt5_headerdir} ; do
 d=%{buildroot}$qtdir/QtSolutions ;
 mkdir -p $d ;
 cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    $d ;
done

install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt4_datadir}/mkspecs/features/qtsingleapplication.prf
install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt5_archdatadir}/mkspecs/features/qtsingleapplication.prf
install -p -D -m644 %{SOURCE2} %{buildroot}%{_qt4_datadir}/mkspecs/features/qtsinglecoreapplication.prf
install -p -D -m644 %{SOURCE2} %{buildroot}%{_qt5_archdatadir}/mkspecs/features/qtsinglecoreapplication.prf


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n qtsinglecoreapplication -p /sbin/ldconfig

%postun -n qtsinglecoreapplication -p /sbin/ldconfig

%files
%license licenses/*
%doc README.TXT
# Caution! Unversioned so file goes into -devel
%{_libdir}/libQtSolutions_SingleApplication*.so.*

%files devel
%doc doc/html/ examples/
%{_libdir}/libQtSolutions_SingleApplication*.so
%dir %{_qt4_headerdir}/QtSolutions/
%{_qt4_headerdir}/QtSolutions/QtSingleApplication
%{_qt4_headerdir}/QtSolutions/%{name}.h
%{_qt4_datadir}/mkspecs/features/qtsingleapplication.prf

%files -n qtsinglecoreapplication
%license licenses/*
# Caution! Unversioned so file goes into -devel
%{_libdir}/libQtSolutions_SingleCoreApplication*.so.*

%files -n qtsinglecoreapplication-devel
%{_libdir}/libQtSolutions_SingleCoreApplication*.so
%dir %{_qt4_headerdir}/QtSolutions/
%{_qt4_headerdir}/QtSolutions/QtSingleCoreApplication
%{_qt4_headerdir}/QtSolutions/qtsinglecoreapplication.h
%{_qt4_datadir}/mkspecs/features/qtsinglecoreapplication.prf

%files qt5
%license licenses/*
%doc README.TXT
# Caution! Unversioned so file goes into -devel
%{_qt5_libdir}/libQt5*SingleApplication*.so.*

%files qt5-devel
%doc doc/html/ examples/
%{_qt5_libdir}/libQt5*SingleApplication*.so
%dir %{_qt5_headerdir}/QtSolutions/
%{_qt5_headerdir}/QtSolutions/QtSingleApplication
%{_qt5_headerdir}/QtSolutions/%{name}.h
%{_qt5_archdatadir}/mkspecs/features/qtsingleapplication.prf

%files -n qtsinglecoreapplication-qt5
%license licenses/*
# Caution! Unversioned so file goes into -devel
%{_qt5_libdir}/libQt5*SingleCoreApplication*.so.*

%files -n qtsinglecoreapplication-qt5-devel
%{_qt5_libdir}/libQt5*SingleCoreApplication*.so
%dir %{_qt5_headerdir}/QtSolutions/
%{_qt5_headerdir}/QtSolutions/QtSingleCoreApplication
%{_qt5_headerdir}/QtSolutions/qtsinglecoreapplication.h
%{_qt5_archdatadir}/mkspecs/features/qtsinglecoreapplication.prf


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.6.1-18
- Rebuild

