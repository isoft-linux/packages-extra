%define username   memcached
%define groupname  memcached

Name:           memcached
Version:        1.4.17
Release:        4%{?dist}
Epoch:          0
Summary:        High Performance, Distributed Memory Object Cache

License:        BSD
URL:            http://www.memcached.org/
Source0:        http://www.memcached.org/files/%{name}-%{version}.tar.gz

# custom unit file
Source1:        memcached.service

# Patches
Patch001:       memcached-manpages.patch

# Fixes

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel systemd-units
BuildRequires:  perl(Test::More), perl(Test::Harness)

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# For triggerun
Requires(pre):  shadow-utils


# as of 3.5.5-4 selinux has memcache included
Obsoletes: memcached-selinux

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%package devel
Summary: Files needed for development using memcached protocol
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.

%prep
%setup -q
%patch001 -p1 -b .manpages

%build
# compile with full RELRO
export CFLAGS="%{optflags} -pie -fpie"
export LDFLAGS="-Wl,-z,relro,-z,now"

%configure
make %{?_smp_mflags}

%check
# whitespace tests fail locally on fedpkg systems now that they use git
rm -f t/whitespace.t

# Parts of the test suite only succeed as non-root.
if [ `id -u` -ne 0 ]; then
  # remove failing test that doesn't work in
  # build systems
  rm -f t/daemonize.t
fi
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool
install -Dp -m0644 scripts/memcached-tool.1 \
        %{buildroot}%{_mandir}/man1/memcached-tool.1

# Unit file
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/memcached.service

# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="%{username}"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# Constant timestamp on the config file.
touch -r %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf %{buildroot}


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
useradd -r -g %{groupname} -d /run/memcached \
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0


%post
%systemd_post memcached.service


%preun
%systemd_preun memcached.service


%postun
%systemd_postun_with_restart memcached.service


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached-tool.1*
%{_mandir}/man1/memcached.1*
%{_unitdir}/memcached.service


%files devel
%defattr(-,root,root,0755)
%{_includedir}/memcached/*

%changelog
