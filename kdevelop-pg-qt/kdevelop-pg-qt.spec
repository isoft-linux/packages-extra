Name:           kdevelop-pg-qt
Summary:        A parser generator 
Version:        1.9.90
Release:        11%{?dist}

# All LGPLv2+, except for bison-generated kdev-pg-parser.{cc.h} which are GPLv2+
License:        LGPLv2+ and GPLv2+ with exception
URL:            http://techbase.kde.org/Development/KDevelop-PG-Qt_Introduction
#git clone git://anongit.kde.org/kdevelop-pg-qt.git
Source0: %{name}.tar.gz

BuildRequires: bison
BuildRequires: flex
BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: qt5-qtbase-devel

%description
KDevelop-PG-Qt is a parser generator written in readable source-code and
generating readable source-code. Its syntax was inspired by AntLR. It
implements the visitor-pattern and uses the Qt library. That is why it
is ideal to be used in Qt-/KDE-based applications like KDevelop.

%package devel
Summary:  Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.


%prep
%autosetup -n %{name} -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files 
%doc AUTHORS COPYING.LIB README
%{_bindir}/kdev-pg-qt

%files devel
%{_includedir}/kdevelop-pg-qt/
%dir %{_libdir}/cmake
%{_libdir}/cmake/KDevelop-PG-Qt/


%changelog
* Fri Nov 25 2016 cjacker - 1.9.90-11
- Update to latest git

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 1.9.90-10
- Initial build

