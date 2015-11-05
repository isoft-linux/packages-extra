#disable the httpd stuff while we're waiting on getting the path issues
#cleared up
%global enable_httpd 1

Name:           web-assets
Version:        5
Release:        4%{?dist}
Summary:        A simple framework for bits pushed to browsers
BuildArch:      noarch

License:        MIT
URL:            https://fedoraproject.org/wiki/User:Patches/PackagingDrafts/Web_Assets

Source1:        LICENSE
Source2:        macros.web-assets
Source3:        web-assets.conf
Source4:        README.devel

%description
%{summary}.

%package filesystem
Summary:        The basic directory layout for Web Assets
#there's nothing copyrightable about a few directories and symlinks
License:        Public Domain

%description filesystem
%{summary}.

%package devel
Summary:        RPM macros for Web Assets packaging
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}

%description devel
%{summary}.

%if 0%{?enable_httpd}
%package httpd
Summary:        Web Assets aliases for the Apache HTTP daemon
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}
Requires:       httpd
Requires(post): systemd
Requires(postun): systemd

%description httpd
%{summary}.
%endif

%prep
%setup -c -T
cp %{SOURCE1} LICENSE
cp %{SOURCE4} README.devel

%build
#nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/web-assets
mkdir -p %{buildroot}%{_datadir}/javascript

ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/javascript
ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/js
ln -sf ../fonts %{buildroot}%{_datadir}/web-assets/fonts

install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.web-assets

%if 0%{?enable_httpd}
install -Dpm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/web-assets.conf

%post httpd
systemctl reload-or-try-restart httpd.service || :

%postun httpd
systemctl reload-or-try-restart httpd.service || :
%endif

%files filesystem
%{_datadir}/web-assets
%{_datadir}/javascript

%files devel
%{_rpmconfigdir}/macros.d/macros.web-assets
%doc LICENSE README.devel

%if 0%{?enable_httpd}
%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/web-assets.conf
%doc LICENSE
%endif

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 5-4
- Initial build

