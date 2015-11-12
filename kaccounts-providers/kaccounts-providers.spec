Name: kaccounts-providers
Version: 15.08.3
Release: 2%{?dist}
Summary: Additional service providers for KAccounts framework
License: GPLv2
URL: https://projects.kde.org/projects/kde/kdenetwork/kaccounts-providers
BuildArch:      noarch

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kaccounts-integration-devel

BuildRequires:  intltool
BuildRequires:  libaccounts-glib-devel

Requires:       signon-ui

%description
%{summary}.

%prep
%setup -q -n kaccounts-providers-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%license COPYING
%{_datadir}/accounts/providers/*.provider
%config %{_sysconfdir}/signon-ui/webkit-options.d/*

%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 15.08.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 15.04.3-2
- Rebuild

