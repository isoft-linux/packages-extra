Name:    poxml
Summary: Text utilities from kdesdk
Version: 15.12.0
Release: 2

License: GPLv2+
URL:     http://www.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz
Patch0: poxml-fix-cmake.patch

BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: gettext-devel
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kdoctools-devel
BuildRequires: qt5-qtbase-devel qt5-qttools-devel

BuildRequires:  pkgconfig(libxslt)
Provides:       kdesdk-poxml = %{version}-%{release}

%description
Text utilities from kdesdk, including
po2xml
split2po
swappo
xml2pot

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

# seeing failures, appear to be parallel-build races
make -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%doc COPYING COPYING.DOC
%{_kf5_bindir}/po2xml
%{_kf5_bindir}/split2po
%{_kf5_bindir}/swappo
%{_kf5_bindir}/xml2pot
%{_mandir}/man1/po2xml*
%{_mandir}/man1/split2po*
%{_mandir}/man1/swappo*
%{_mandir}/man1/xml2pot*


%changelog
* Thu Dec 17 2015 Cjacker <cjacker@foxmail.com> - 15.12.0-2
- Update

* Sat Nov 21 2015 Cjacker <cjacker@foxmail.com> - 15.11.80-2
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.08.2-3
- Rebuild

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2
