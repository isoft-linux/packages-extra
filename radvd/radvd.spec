Summary: A Router Advertisement daemon
Name: radvd
Version: 2.11
Release: 1%{?dist}
# The code includes the advertising clause, so it's GPL-incompatible
License: BSD with advertising
Group: System Environment/Daemons
URL: http://www.litech.org/radvd/
Source0: %{url}dist/%{name}-%{version}.tar.xz
Source1: radvd-tmpfs.conf
Source2: radvd.service
# radvdump: show routes with prefixlen > 64
#
# https://bugzilla.redhat.com/show_bug.cgi?id=1188891
# https://github.com/reubenhwk/radvd/pull/42
#
# Submitted upstream.
Patch0: radvd-2.11-route-info.patch
BuildRequires: bison
BuildRequires: flex
#BuildRequires: flex-static
BuildRequires: pkgconfig
BuildRequires: check-devel
BuildRequires: systemd-units
Requires(postun): systemd-units
Requires(preun): systemd-units
Requires(post): systemd-units
Requires(pre): shadow-utils

%description
radvd is the router advertisement daemon for IPv6.  It listens to router
solicitations and sends router advertisements as described in "Neighbor
Discovery for IP Version 6 (IPv6)" (RFC 2461).  With these advertisements
hosts can automatically configure their addresses and some other
parameters.  They also can choose a default router based on these
advertisements.

Install radvd if you are setting up IPv6 network and/or Mobile IPv6
services.

%prep
%setup -q
%patch0 -p1
for F in CHANGES; do
    iconv -f iso-8859-1 -t utf-8 < "$F" > "${F}.new"
    touch -r "$F" "${F}.new"
    mv "${F}.new" "$F"
done

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIE" 
export LDFLAGS='-pie -Wl,-z,relro,-z,now,-z,noexecstack,-z,nodlopen'
%configure \
    --disable-silent-rules \
    --with-pidfile=%{_localstatedir}/run/radvd/radvd.pid
make %{?_smp_mflags} 

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/radvd
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

install -m 644 redhat/radvd.conf.empty $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf
install -m 644 redhat/radvd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/radvd

install -d -m 755 $RPM_BUILD_ROOT%{_tmpfilesdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_tmpfilesdir}/radvd.conf
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_unitdir}

%check
# The tests don't work, see https://github.com/reubenhwk/radvd/issues/30
#make check

%postun
%systemd_postun_with_restart radvd.service

%post
%systemd_post radvd.service

%preun
%systemd_preun radvd.service

# Static UID and GID defined by /usr/share/doc/setup-*/uidgid
%pre
getent group radvd >/dev/null || groupadd -r -g 75 radvd
getent passwd radvd >/dev/null || \
  useradd -r -u 75 -g radvd -d / -s /sbin/nologin -c "radvd user" radvd
exit 0

%files
%doc CHANGES COPYRIGHT INTRO.html README TODO
%{_unitdir}/radvd.service
%config(noreplace) %{_sysconfdir}/radvd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/radvd
%{_tmpfilesdir}/radvd.conf
%dir %attr(-,radvd,radvd) %{_localstatedir}/run/radvd/
%doc radvd.conf.example
%{_mandir}/*/*
%{_sbindir}/radvd
%{_sbindir}/radvdump

%changelog
* Wed Apr 27 2016 fj <fujiang.zhu@isoft.com.cn> - 2.11-1
- add for libvirt



