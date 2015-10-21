Name:    poxml
Summary: Text utilities from kdesdk
Version: 15.08.2
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

BuildRequires:  kdelibs-devel >= 4.14
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(libxslt)

Conflicts:      kdesdk-common < 4.10.80
Provides:       kdesdk-poxml = %{version}-%{release}
Obsoletes:      kdesdk-poxml < 4.10.80


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
%{cmake_kde4} ..
popd

# seeing failures, appear to be parallel-build races
make -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%doc COPYING COPYING.DOC
%{_kde4_bindir}/po2xml
%{_kde4_bindir}/split2po
%{_kde4_bindir}/swappo
%{_kde4_bindir}/xml2pot
%{_mandir}/man1/po2xml*
%{_mandir}/man1/split2po*
%{_mandir}/man1/swappo*
%{_mandir}/man1/xml2pot*


%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- update to 15.08.2
