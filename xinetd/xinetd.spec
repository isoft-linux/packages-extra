Summary: A secure replacement for inetd
Name: xinetd
Version: 2.3.15
Release: 17%{?dist}
License: xinetd
Epoch: 2
URL: https://github.com/xinetd-org/xinetd
# source can be downloaded at
# https://github.com/xinetd-org/xinetd/archive/xinetd-2-3-15.tar.gz
Source: xinetd-%{version}.tar.gz
Source1: xinetd.service
Patch0: xinetd-2.3.15-pie.patch
Patch4: xinetd-2.3.14-bind-ipv6.patch
Patch6: xinetd-2.3.14-man-section.patch
Patch7: xinetd-2.3.15-PIE.patch
Patch8: xinetd-2.3.14-ident-bind.patch
Patch9: xinetd-2.3.14-readable-debuginfo.patch
# Patch for clean reconfiguration using newer versions of autotools
Patch10: xinetd-2.3.14-autoconf.patch
# Completely rewritten socket handling code (it uses poll() instead
# of select() function)
Patch11: xinetd-2.3.14-poll.patch
# New configuration option (limit for files opened by child process)
Patch12: xinetd-2.3.14-file-limit.patch
# When using tcpmux, xinetd ended up with sigsegv
# (detection of NULL pointer in pollfd structure was missing)
Patch13: xinetd-2.3.14-tcpmux.patch
# When service is destroyed, destroy also its
# file descriptor in array given to poll function
Patch14: xinetd-2.3.14-clean-pfd.patch
# xinetd confuses ipv6 and ipv4 port parsing
# - furtunately, they have the same format, so everything
#   works even without this patch
Patch15: xinetd-2.3.14-ipv6confusion.patch
# This fixes bug #593904 - online reconfiguration caused log message
# flood when turning off UDP service
Patch16: xinetd-2.3.14-udp-reconfig.patch
Patch18: xinetd-2.3.14-rpc-specific-port.patch
Patch19: xinetd-2.3.14-signal-log-hang.patch
Patch20: xinetd-2.3.14-fix-type-punned-ptr.patch
# Fix leaking file descriptors and pfd_array wasting
# This fixes #702670
Patch21: xinetd-2.3.14-leaking-fds.patch
# Fix memory corruption when loading a large number of services
# This fixes #720390
Patch22: xinetd-2.3.14-many-services.patch
# Remove realloc of fds that was causing memory corruption
Patch23: xinetd-2.3.14-realloc-remove.patch
# Fix leaking descriptor when starting a service fails
Patch24: xinetd-2.3.14-leaking-fds-2a.patch
# Fix #770858 - Instances limit in xinetd can be easily bypassed
Patch25: xinetd-2.3.14-instances.patch
# Fix #809272 - Service disabled due to bind failure
Patch26: xinetd-2.3.14-retry-svc-activate-in-cps-restart.patch
Patch27: xinetd-2.3.15-bad-port-check.patch
Patch29: xinetd-2.3.15-creds.patch
# Fix #1033528 - xinetd segfaults when connecting to tcpmux service
Patch30: xinetd-2.3.15-tcpmux-nameinargs-disable-service.patch

BuildRequires: autoconf, automake
BuildRequires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{!?tcp_wrappers:BuildRequires: tcp_wrappers-devel}
Requires: filesystem >= 2.0.1, setup, fileutils
Provides: inetd


%description
Xinetd is a secure replacement for inetd, the Internet services
daemon. Xinetd provides access control for all services based on the
address of the remote host and/or on time of access and can prevent
denial-of-access attacks. Xinetd provides extensive logging, has no
limit on the number of server arguments, and lets you bind specific
services to specific IP addresses on your host machine. Each service
has its own specific configuration file for Xinetd; the files are
located in the /etc/xinetd.d directory.

%prep
%setup -q

# SPARC/SPARC64 needs -fPIE/-PIE
# This really should be detected by configure.
%ifarch sparcv9 sparc64
%patch7 -p1 -b .PIE
%else
%patch0 -p1 -b .pie
%endif
%patch4 -p1 -b .bind
%patch6 -p1 -b .man-section
%patch8 -p1 -b .ident-bind
%patch9 -p1 -b .readable-debuginfo
%patch10 -p1 -b .autoconf
%patch11 -p1 -b .poll
%patch12 -p1 -b .file-limit
%patch13 -p1 -b .tcpmux
%patch14 -p1 -b .clean-pfd
%patch15 -p1 -b .ipv6confusion
%patch16 -p1 -b .udp-reconfig
%patch18 -p1 -b .rpc-specific-port
%patch19 -p1 -b .signal-log-hang
%patch20 -p1 -b .fix-type-punned-ptr
%patch21 -p1 -b .leaking-fds
%patch22 -p1 -b .many-services
%patch23 -p1 -b .realloc-remove
%patch24 -p1 -b .leaking-fds-2a
%patch25 -p1 -b .instances
%patch26 -p1 -b .retry-svc-activate
%patch27 -p1 -b .bad-port-check
%patch29 -p1 -b .creds
%patch30 -p1

aclocal
autoconf

%build
# -pie -PIE flags added by separate patches
export LDFLAGS="$LDFLAGS -Wl,-z,relro,-z,now"
%configure --with-loadavg --with-inet6 %{!?tcp_wrappers:--with-libwrap} --with-labeled-networking
make

%install
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -m 700 -p $RPM_BUILD_ROOT/etc/xinetd.d/
# Remove unneeded service
rm -f contrib/xinetd.d/ftp-sensor
%make_install DAEMONDIR=$RPM_BUILD_ROOT/usr/sbin MANDIR=$RPM_BUILD_ROOT/%{_mandir}
install -m 600 contrib/xinetd.conf $RPM_BUILD_ROOT/etc
install -m 600 contrib/xinetd.d/* $RPM_BUILD_ROOT/etc/xinetd.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}

rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/itox*
rm -f $RPM_BUILD_ROOT/usr/sbin/itox
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/xconv.pl*
rm -f $RPM_BUILD_ROOT/usr/sbin/xconv.pl

%post
%systemd_post xinetd.service

%preun
%systemd_preun xinetd.service

%postun
%systemd_postun_with_restart xinetd.service

%files
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf
%config(noreplace) /etc/xinetd.conf
%{_unitdir}/xinetd.service
%config(noreplace) /etc/xinetd.d/*
/usr/sbin/xinetd
%{_mandir}/*/*

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2:2.3.15-17
- Initial build

