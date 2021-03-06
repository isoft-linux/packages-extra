%global _hardened_build 1
%global with_perftools 0

%global with_systemd 1

# Tests fail in mock, not in local build.
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:              redis
Version:           3.0.6
Release:           4%{?dist}
Summary:           A persistent key-value database
License:           BSD
URL:               http://redis.io
Source0:           http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:           %{name}.logrotate
Source2:           %{name}-sentinel.service
Source3:           %{name}.service
Source4:           %{name}.tmpfiles
Source5:           %{name}-sentinel.init
Source6:           %{name}.init
Source7:           %{name}-shutdown
Source8:           %{name}-limit-systemd
Source9:           %{name}-limit-init
# To refresh patches:
# tar xf redis-xxx.tar.gz && cd redis-xxx && git init && git add . && git commit -m "%{version} baseline"
# git am %{patches}
# Then refresh your patches
# git format-patch HEAD~<number of expected patches>
# Update configuration for Fedora
Patch0001:            0001-redis-2.8.18-redis-conf.patch
Patch0002:            0002-redis-2.8.18-deps-library-fPIC-performance-tuning.patch
Patch0003:            0003-redis-2.8.18-use-system-jemalloc.patch
# tests/integration/replication-psync.tcl failed on slow machines(GITHUB #1417)
Patch0004:            0004-redis-2.8.18-disable-test-failed-on-slow-machine.patch
# Fix sentinel configuration to use a different log file than redis
Patch0005:            0005-redis-2.8.18-sentinel-configuration-file-fix.patch
%if 0%{?with_perftools}
BuildRequires:     gperftools-devel
%else
BuildRequires:     jemalloc-devel
%endif
%if 0%{?with_tests}
BuildRequires:     procps-ng
%endif
%if 0%{?with_systemd}
BuildRequires:     systemd
%endif
%if 0%{?with_tests}
BuildRequires:     tcl
%endif
# Required for redis-shutdown
Requires:          /bin/awk
Requires:          logrotate
Requires(pre):     shadow-utils
%if 0%{?with_systemd}
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

%description
Redis is an advanced key-value store. It is often referred to as a data 
structure server since keys can contain strings, hashes, lists, sets and 
sorted sets.

You can run atomic operations on these types, like appending to a string;
incrementing the value in a hash; pushing to a list; computing set 
intersection, union and difference; or getting the member with highest 
ranking in a sorted set.

In order to achieve its outstanding performance, Redis works with an 
in-memory dataset. Depending on your use case, you can persist it either 
by dumping the dataset to disk every once in a while, or by appending 
each command to a log.

Redis also supports trivial-to-setup master-slave replication, with very 
fast non-blocking first synchronization, auto-reconnection on net split 
and so forth.

Other features include Transactions, Pub/Sub, Lua scripting, Keys with a 
limited time-to-live, and configuration settings to make Redis behave like 
a cache.

You can use Redis from most programming languages also.

%prep
%setup -q
rm -frv deps/jemalloc
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1

# No hidden build.
sed -i -e 's|\t@|\t|g' deps/lua/src/Makefile
sed -i -e 's|$(QUIET_CC)||g' src/Makefile
sed -i -e 's|$(QUIET_LINK)||g' src/Makefile
sed -i -e 's|$(QUIET_INSTALL)||g' src/Makefile
# Ensure deps are built with proper flags
sed -i -e 's|$(CFLAGS)|%{optflags}|g' deps/Makefile
sed -i -e 's|OPTIMIZATION?=-O3|OPTIMIZATION=%{optflags}|g' deps/hiredis/Makefile
sed -i -e 's|$(LDFLAGS)|%{?__global_ldflags}|g' deps/hiredis/Makefile
sed -i -e 's|$(CFLAGS)|%{optflags}|g' deps/linenoise/Makefile
sed -i -e 's|$(LDFLAGS)|%{?__global_ldflags}|g' deps/linenoise/Makefile

%build
make %{?_smp_mflags} \
    DEBUG="" \
    LDFLAGS="%{?__global_ldflags}" \
    CFLAGS+="%{optflags}" \
    LUA_LDFLAGS+="%{?__global_ldflags}" \
%if 0%{?with_perftools}
    MALLOC=tcmalloc \
%else
    MALLOC=jemalloc \
%endif
    all

%install
make install INSTALL="install -p" PREFIX=%{buildroot}%{_prefix}

# Filesystem.
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/run/%{name}

# Install logrotate file.
install -pDm644 %{S:1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install configuration files.
install -pDm644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -pDm644 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}-sentinel.conf

# Install Systemd unit files.
%if 0%{?with_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -pm644 %{S:3} %{buildroot}%{_unitdir}
install -pm644 %{S:2} %{buildroot}%{_unitdir}

# Install systemd tmpfiles config.
install -pDm644 %{S:4} %{buildroot}%{_tmpfilesdir}/%{name}.conf
# Install systemd limit files (requires systemd >= 204)
install -p -D -m 644 %{S:8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -p -D -m 644 %{S:8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else # install SysV service files
install -pDm755 %{S:5} %{buildroot}%{_initrddir}/%{name}-sentinel
install -pDm755 %{S:6} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 644 %{S:9} %{buildroot}%{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif

# Fix non-standard-executable-perm error.
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# create redis-sentinel command as described on
# http://redis.io/topics/sentinel
ln -sf %{name}-server %{buildroot}%{_bindir}/%{name}-sentinel

# Install redis-shutdown
install -pDm755 %{S:7} %{buildroot}%{_bindir}/%{name}-shutdown

%check
%if 0%{?with_tests}
make test ||:
make test-sentinel ||:
%endif

%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null
exit 0

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%systemd_post %{name}-sentinel.service
%else
chkconfig --add %{name}
chkconfig --add %{name}-sentinel
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%systemd_preun %{name}-sentinel.service
%else
if [ $1 -eq 0 ] ; then
    service %{name} stop &> /dev/null
    chkconfig --del %{name} &> /dev/null
    service %{name}-sentinel stop &> /dev/null
    chkconfig --del %{name}-sentinel &> /dev/null
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-sentinel.service
%else
if [ "$1" -ge "1" ] ; then
    service %{name} condrestart >/dev/null 2>&1 || :
    service %{name}-sentinel condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc 00-RELEASENOTES BUGS CONTRIBUTING MANIFESTO README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}-sentinel.conf
%dir %attr(0755, redis, redis) %{_sharedstatedir}/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%if 0%{?with_systemd}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service
%dir %{_sysconfdir}/systemd/system/%{name}.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%dir %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else
%{_initrddir}/%{name}
%{_initrddir}/%{name}-sentinel
%config(noreplace) %{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif


%changelog
* Tue Mar 22 2016 <sulit> <sulitsrc@gmail.com> - 3.0.6-4
- Init for isoft5

