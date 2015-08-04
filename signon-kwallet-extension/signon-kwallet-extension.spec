Name:           signon-kwallet-extension
Version: 15.04.3
Release: 1%{?dist}
Summary:        KWallet integration for Sign-on framework

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/kdenetwork/signon-kwallet-extension

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

# Upstream patches (https://git.reviewboard.kde.org/r/123148/)
Patch0:         signon-kwallet-extension-drop-lib-soname.patch

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kwallet-devel
BuildRequires:  signon-devel

%description
%{summary}.


%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .soname

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/signon/extensions/libkeyring-kwallet.so

%changelog
