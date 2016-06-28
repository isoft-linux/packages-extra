Name:           isns-utils
Version:        0.94
Release:        2
Summary:        The iSNS daemon and utility programs

Group:          System Environment/Daemons
License:        LGPLv2+
URL:            https://github.com/gonzoleeman/open-isns
Source0:        https://github.com/gonzoleeman/open-isns/archive/%{version}.tar.gz#/open-isns-%{version}.tar.gz
Source1:        isnsd.service

BuildRequires:  openssl-devel automake pkgconfig systemd-devel systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.


%package devel
Group: Development/Libraries
Summary: Development files for iSNS

%description devel
Development files for iSNS


%prep
%setup -q -n open-isns-%{version}


%build
%configure
make %{?_smp_mflags}


%install
sed -i -e 's|-m 555|-m 755|' Makefile
make install DESTDIR=%{buildroot}
make install_hdrs DESTDIR=%{buildroot}
make install_lib DESTDIR=%{buildroot}
rm %{buildroot}%{_unitdir}/isnsd.service
rm %{buildroot}%{_unitdir}/isnsd.socket
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/isnsd.service


%post
%systemd_post isnsd.service


%postun
%systemd_postun isnsd.service


%preun
%systemd_preun isnsd.service


%triggerun -- isns-utils < 0.91-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save isnsd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del isnsd >/dev/null 2>&1 || :
/bin/systemctl try-restart isnsd.service >/dev/null 2>&1 || :


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_mandir}/man8/*
%{_unitdir}/isnsd.service
%dir %{_sysconfdir}/isns
%dir %{_var}/lib/isns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/isns/*


%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/libisns
%{_includedir}/libisns/*.h
%{_libdir}/libisns.a


%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 0.94-2
- rebuilt for libvirt

