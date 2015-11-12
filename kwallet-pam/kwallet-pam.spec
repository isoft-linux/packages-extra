Name:    kwallet-pam
Summary: PAM module for KWallet
Version: 5.4.3
Release: 2 

License: LGPLv2+
URL:     http://www.kde.org/

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires: cmake >= 2.8
BuildRequires: libgcrypt-devel >= 1.5.0
BuildRequires: pam-devel

Requires: socat

%description
%{summary}.


%prep
%setup -q 


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
mv %{buildroot}/%{_lib}/security/pam_kwallet5.so %{buildroot}/%{_lib}/security/pam_kwallet.so

%files
/%{_lib}/security/pam_kwallet.so


%changelog
* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 5.4.3-2
- Update to 5.4.3, and move from kde to extra, we do not ship it by default

* Sun Oct 25 2015 Cjacker <cjacker@foxmail.com> - 5.4.2-2
- Rebuild for new 4.0 release

* Wed Oct 07 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.2

* Wed Sep 09 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.1

* Wed Aug 26 2015 Cjacker <cjacker@foxmail.com>
- update to 5.4.0

* Thu Jul 16 2015 Cjacker <cjacker@foxmail.com>
- patch to meet kwalletd kf5 requires.
