%global open_iscsi_version	2.0
%global open_iscsi_build	873
%global commit0 		4c9d6f9908bc55e4514b00c178ae72bb0d8fc96b
%global shortcommit0		%(c=%{commit0}; echo ${c:0:7})

Summary: iSCSI daemon and utility programs
Name: iscsi-initiator-utils
Version: 6.%{open_iscsi_version}.%{open_iscsi_build}
Release: 30.git%{shortcommit0}%{?dist}
Group: System Environment/Daemons
License: GPLv2+
URL: http://www.open-iscsi.org
Source0: https://github.com/mikechristie/open-iscsi/archive/%{commit0}.tar.gz#/open-iscsi-%{shortcommit0}.tar.gz
Source4: 04-iscsi
Source5: iscsi-tmpfiles.conf

Patch1: open-iscsi-v2.0.873-4c9d6f9-1-idmb_rec_write-check-for-tpgt-first.patch
Patch2: open-iscsi-v2.0.873-4c9d6f9-2-idbm_rec_write-seperate-old-and-new-style-writes.patch
Patch3:open-iscsi-v2.0.873-4c9d6f9-3-idbw_rec_write-pick-tpgt-from-existing-record.patch
Patch4:open-iscsi-v2.0.873-4c9d6f9-4-update-systemd-service-files-add-iscsi.service-for-s.patch
Patch5:open-iscsi-v2.0.873-4c9d6f9-5-iscsi-boot-related-service-file-updates.patch
Patch6:open-iscsi-v2.0.873-4c9d6f9-6-update-initscripts-and-docs.patch
Patch7:open-iscsi-v2.0.873-4c9d6f9-7-use-var-for-config.patch
Patch8:open-iscsi-v2.0.873-4c9d6f9-8-use-red-hat-for-name.patch
Patch9:open-iscsi-v2.0.873-4c9d6f9-9-libiscsi.patch
Patch10:open-iscsi-v2.0.873-4c9d6f9-10-remove-the-offload-boot-supported-ifdef.patch
Patch11:open-iscsi-v2.0.873-4c9d6f9-11-iscsiuio-systemd-unit-files.patch
Patch12:open-iscsi-v2.0.873-4c9d6f9-12-disable-iscsid.startup-from-iscsiadm-prefer-systemd-.patch
Patch13:open-iscsi-v2.0.873-4c9d6f9-13-Don-t-check-for-autostart-sessions-if-iscsi-is-not-u.patch
Patch14:open-iscsi-v2.0.873-4c9d6f9-14-start-socket-listeners-on-iscsiadm-command.patch
Patch15:open-iscsi-v2.0.873-4c9d6f9-15-Revert-iscsiadm-return-error-when-login-fails.patch
Patch16:open-iscsi-v2.0.873-4c9d6f9-16-update-handling-of-boot-sessions.patch
Patch17:open-iscsi-v2.0.873-4c9d6f9-17-update-iscsi.service-for-boot-session-recovery.patch
Patch18:open-iscsi-v2.0.873-4c9d6f9-18-updates-to-iscsi.service.patch
Patch19:open-iscsi-v2.0.873-4c9d6f9-19-make-session-shutdown-a-seperate-service.patch.patch
Patch20:open-iscsi-v2.0.873-4c9d6f9-20-Add-macros-to-release-GIL-lock.patch
Patch21:open-iscsi-v2.0.873-4c9d6f9-21-libiscsi-introduce-sessions-API.patch
# ugly version string patch, should change with every rebuild
Patch22:open-iscsi-v2.0.873-4c9d6f9-22-use-Red-Hat-version-string-to-match-RPM-package-vers.patch
Patch23:open-iscsi-v2.0.873-4c9d6f9-23-add-libslp-in-makefile.patch

BuildRequires: flex bison python2-devel python3-devel python-setuptools doxygen kmod-devel systemd-units
BuildRequires: autoconf automake libtool libmount-devel isns-utils-devel openssl-devel openslp openslp-devel
# For dir ownership
Requires: %{name}-iscsiuio >= %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%global _hardened_build 1
%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so|%{python3_sitearch}/.*\\.so)$

%description
The iscsi package provides the server daemon for the iSCSI protocol,
as well as the utility programs used to manage it. iSCSI is a protocol
for distributed disk access using SCSI commands sent over Internet
Protocol networks.

%package iscsiuio
Summary: Userspace configuration daemon required for some iSCSI hardware
Group: System Environment/Daemons
License: BSD
Requires: %{name} = %{version}-%{release}

%description iscsiuio
The iscsiuio configuration daemon provides network configuration help
for some iSCSI offload hardware.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python-%{name}
Summary: Python %{python2_version} bindings to %{name}
Group: Development/Libraries

%description -n python-%{name}
The %{name}-python2 package contains Python %{python2_version} bindings to the
libiscsi interface for interacting with %{name}

%package -n python3-%{name}
Summary: Python %{python3_version} bindings to %{name}
Group: Development/Libraries

%description -n python3-%{name}
The %{name}-python3 package contains Python %{python3_version} bindings to the
libiscsi interface for interacting with %{name}

%prep
%autosetup -p1 -n open-iscsi-%{commit0}

# change exec_prefix, there's no easy way to override
%{__sed} -i -e 's|^exec_prefix = /$|exec_prefix = %{_exec_prefix}|' Makefile

%build

# configure sub-packages from here
# letting the top level Makefile do it will lose setting from rpm
cd iscsiuio
autoreconf --install
%{configure}
cd ..

%{__make} OPTFLAGS="%{optflags} %{?__global_ldflags} -DUSE_KMOD -lkmod"
pushd libiscsi
%{__python2} setup.py build
%{__python3} setup.py build
touch -r libiscsi.doxy html/*
popd


%install
%{__make} DESTDIR=%{?buildroot} install_programs install_doc install_etc
# upstream makefile doesn't get everything the way we like it
rm $RPM_BUILD_ROOT%{_sbindir}/iscsi_discovery
rm $RPM_BUILD_ROOT%{_mandir}/man8/iscsi_discovery.8
%{__install} -pm 755 usr/iscsistart $RPM_BUILD_ROOT%{_sbindir}
%{__install} -pm 644 doc/iscsistart.8 $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -pm 644 doc/iscsi-iname.8 $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -pm 644 iscsiuio/iscsiuiolog $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d

%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/nodes
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/send_targets
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/static
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/isns
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/slp
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/ifaces

# for %%ghost
%{__install} -d $RPM_BUILD_ROOT/var/lock/iscsi
touch $RPM_BUILD_ROOT/var/lock/iscsi/lock


%{__install} -d $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi-shutdown.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsid.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsid.socket $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsiuio.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsiuio.socket $RPM_BUILD_ROOT%{_unitdir}

%{__install} -d $RPM_BUILD_ROOT%{_libexecdir}
%{__install} -pm 755 etc/systemd/iscsi-mark-root-nodes $RPM_BUILD_ROOT%{_libexecdir}

%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d
%{__install} -pm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d

%{__install} -d $RPM_BUILD_ROOT%{_tmpfilesdir}
%{__install} -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_tmpfilesdir}/iscsi.conf

%{__install} -d $RPM_BUILD_ROOT%{_libdir}
%{__install} -pm 755 libiscsi/libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}
%{__ln_s}    libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}/libiscsi.so
%{__install} -d $RPM_BUILD_ROOT%{_includedir}
%{__install} -pm 644 libiscsi/libiscsi.h $RPM_BUILD_ROOT%{_includedir}

%{__install} -d $RPM_BUILD_ROOT%{python2_sitearch}
%{__install} -d $RPM_BUILD_ROOT%{python3_sitearch}
pushd libiscsi
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


%post
/sbin/ldconfig

%systemd_post iscsi.service iscsi-shutdown.service iscsid.service iscsid.socket

if [ $1 -eq 1 ]; then
	if [ ! -f %{_sysconfdir}/iscsi/initiatorname.iscsi ]; then
		echo "InitiatorName=`/usr/sbin/iscsi-iname`" > %{_sysconfdir}/iscsi/initiatorname.iscsi
	fi
	# enable socket activation and persistant session startup by default
	/bin/systemctl enable iscsi.service >/dev/null 2>&1 || :
	/bin/systemctl enable iscsid.socket >/dev/null 2>&1 || :
fi

%post iscsiuio
%systemd_post iscsiuio.service iscsiuio.socket

if [ $1 -eq 1 ]; then
	/bin/systemctl enable iscsiuio.socket >/dev/null 2>&1 || :
fi

%preun
%systemd_preun iscsi.service iscsi-shutdown.service iscsid.service iscsiuio.service iscsid.socket iscsiuio.socket

%preun iscsiuio
%systemd_preun iscsiuio.service iscsiuio.socket

%postun
/sbin/ldconfig
%systemd_postun

%postun iscsiuio
%systemd_postun

%triggerun -- iscsi-initiator-utils < 6.2.0.873-25
# prior to 6.2.0.873-24 iscsi.service was missing a Wants=remote-fs-pre.target
# this forces remote-fs-pre.target active if needed for a clean shutdown/reboot
# after upgrading this package
if [ $1 -gt 0 ]; then
    /usr/bin/systemctl -q is-active iscsi.service
    if [ $? -eq 0 ]; then
        /usr/bin/systemctl -q is-active remote-fs-pre.target
        if [ $? -ne 0 ]; then
            SRC=`/usr/bin/systemctl show --property FragmentPath remote-fs-pre.target | cut -d= -f2`
            DST=/run/systemd/system/remote-fs-pre.target
            if [ $SRC != $DST ]; then
                cp $SRC $DST
            fi
            sed -i 's/RefuseManualStart=yes/RefuseManualStart=no/' $DST
            /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
            /usr/bin/systemctl start remote-fs-pre.target >/dev/null 2>&1 || :
        fi
    fi
fi
# added in 6.2.0.873-25
if [ $1 -gt 0 ]; then
    systemctl start iscsi-shutdown.service >/dev/null 2>&1 || :
fi


%files
%doc README
%dir %{_sharedstatedir}/iscsi
%dir %{_sharedstatedir}/iscsi/nodes
%dir %{_sharedstatedir}/iscsi/isns
%dir %{_sharedstatedir}/iscsi/static
%dir %{_sharedstatedir}/iscsi/slp
%dir %{_sharedstatedir}/iscsi/ifaces
%dir %{_sharedstatedir}/iscsi/send_targets
%ghost %{_var}/lock/iscsi
%ghost %{_var}/lock/iscsi/lock
%{_unitdir}/iscsi.service
%{_unitdir}/iscsi-shutdown.service
%{_unitdir}/iscsid.service
%{_unitdir}/iscsid.socket
%{_libexecdir}/iscsi-mark-root-nodes
%{_sysconfdir}/NetworkManager/dispatcher.d/04-iscsi
%{_tmpfilesdir}/iscsi.conf
%dir %{_sysconfdir}/iscsi
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
%{_sbindir}/iscsi-iname
%{_sbindir}/iscsiadm
%{_sbindir}/iscsid
%{_sbindir}/iscsistart
%{_libdir}/libiscsi.so.0
%{_mandir}/man8/iscsi-iname.8.gz
%{_mandir}/man8/iscsiadm.8.gz
%{_mandir}/man8/iscsid.8.gz
%{_mandir}/man8/iscsistart.8.gz

%files iscsiuio
%{_sbindir}/iscsiuio
%{_unitdir}/iscsiuio.service
%{_unitdir}/iscsiuio.socket
%config(noreplace) %{_sysconfdir}/logrotate.d/iscsiuiolog
%{_mandir}/man8/iscsiuio.8.gz

%files devel
%doc libiscsi/html
%{_libdir}/libiscsi.so
%{_includedir}/libiscsi.h

%files -n python-%{name}
%{python2_sitearch}/*

%files -n python3-%{name}
%{python3_sitearch}/*

%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 6.2.0.873-30.git4c9d6f9
- rebuilt for libvirt

