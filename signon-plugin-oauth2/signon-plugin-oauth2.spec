Name:           signon-plugin-oauth2
Version:        0.22
Release:        2%{?dist}
Summary:        OAuth2 plugin for the Accounts framework

License:        LGPLv2
URL:            https://gitlab.com/accounts-sso/signon-plugin-oauth2

Source0:        https://gitlab.com/accounts-sso/signon-plugin-oauth2/repository/archive.tar.gz?ref=VERSION_%{version}#/%{name}-%{version}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  signon-devel
BuildRequires:  doxygen
BuildRequires:  libproxy-devel

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%prep
%setup -q -n %{name}.git

sed -i 's/-Werror//g' common-project-config.pri

%build
export PATH=%{_qt5_bindir}:$PATH
qmake-qt5 QMF_INSTALL_ROOT=%{_prefix} \
    CONFIG+=release \
    LIBDIR=%{?_libdir} \
    signon-oauth2.pro

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# Delete tests
rm -fv %{buildroot}/%{_bindir}/signon-oauth2plugin-tests
rm -rfv %{buildroot}/%{_datadir}/signon-oauth2plugin-tests

# Delete examples
rm -fv %{buildroot}/%{_bindir}/oauthclient
rm -rvf %{buildroot}/%{_sysconfdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/signon/liboauth2plugin.so

%files devel
%{_includedir}/signon-plugins/*.h
%{_libdir}/pkgconfig/signon-oauth2plugin.pc


%changelog
