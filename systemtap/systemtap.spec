%define initdir %{_initddir}
%define dracutstap %{_prefix}/lib/dracut/modules.d/99stap

Name: systemtap
Version: 3.0
Release: 0.20151027git8136768%{?dist}
Summary: Programmable system-wide instrumentation system
License: GPLv2+
URL: http://sourceware.org/systemtap/
Source: %{name}-%{version}-0.20151026git8136768.tar.gz

BuildRequires: gcc-c++
BuildRequires: gettext-devel
BuildRequires: nss-devel avahi-devel pkgconfig
BuildRequires: sqlite-devel
BuildRequires: boost-devel
BuildRequires: zlib-devel
BuildRequires: librpm-devel glibc-headers
BuildRequires: libelfutils-devel
BuildRequires: xmlto

# Install requirements
Requires: systemtap-client = %{version}-%{release}
Requires: systemtap-devel = %{version}-%{release}

%description
SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system.  The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

%package server
Summary: Instrumentation System Server
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires: systemtap-devel = %{version}-%{release}
Requires: nss
#for mktemp
Requires: coreutils
Requires: zip unzip
Requires(pre): shadow-utils
BuildRequires: nss-devel avahi-devel
Requires: openssl

%description server
This is the remote script compilation server component of systemtap.
It announces itself to nearby clients with avahi (if available), and
compiles systemtap scripts to kernel objects on their demand.


%package devel
Summary: Programmable system-wide instrumentation system - development headers, tools
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires: kernel-devel
Requires: gcc make
# Suggest: kernel-debuginfo

%description devel
This package contains the components needed to compile a systemtap
script from source form into executable (.ko) forms.  It may be
installed on a self-contained developer workstation (along with the
systemtap-client and systemtap-runtime packages), or on a dedicated
remote server (alongside the systemtap-server package).  It includes
a copy of the standard tapset library and the runtime library C files.

%package runtime
Summary: Programmable system-wide instrumentation system - runtime
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires(pre): shadow-utils

%description runtime
SystemTap runtime contains the components needed to execute
a systemtap script that was already compiled into a module
using a local or remote systemtap-devel installation.


%package client
Summary: Programmable system-wide instrumentation system - client
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires: zip unzip
Requires: systemtap-runtime = %{version}-%{release}
Requires: coreutils grep sed unzip zip
Requires: openssh-clients

%description client
This package contains/requires the components needed to develop
systemtap scripts, and compile them using a local systemtap-devel
or a remote systemtap-server installation, then run them using a
local or remote systemtap-runtime.  It includes script samples and
documentation, and a copy of the tapset library for reference.


%package initscript
Summary: Systemtap Initscripts
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires: systemtap = %{version}-%{release}

%description initscript
This package includes a SysVinit script to launch selected systemtap
scripts at system startup, along with a dracut module for early
boot-time probing if supported.


%package sdt-devel
Summary: Static probe support tools
License: GPLv2+ and Public Domain
URL: http://sourceware.org/systemtap/
Requires: python3-pyparsing

%description sdt-devel
This package includes the <sys/sdt.h> header file used for static
instrumentation compiled into userspace programs and libraries, along
with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.


%package testsuite
Summary: Instrumentation System Testsuite
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires: systemtap = %{version}-%{release}
Requires: systemtap-sdt-devel = %{version}-%{release}
Requires: systemtap-server = %{version}-%{release}
Requires: dejagnu which elfutils grep nc
Requires: gcc make glibc-devel
# testsuite/systemtap.base/ptrace.exp needs strace
Requires: strace
# testsuite/systemtap.base/ipaddr.exp needs nc. Unfortunately, the rpm
# that provides nc has changed over time (from 'nc' to
# 'nmap-ncat'). So, we'll do a file-based require.
Requires: /usr/bin/nc
# testsuite/systemtap.server/client.exp needs avahi
Requires: avahi

# The following "meta" files for the systemtap examples run "perf":
#   testsuite/systemtap.examples/hw_watch_addr.meta
#   testsuite/systemtap.examples/memory/hw_watch_sym.meta
Requires: perf

%description testsuite
This package includes the dejagnu-based systemtap stress self-testing
suite.  This may be used by system administrators to thoroughly check
systemtap on the current system.


# ------------------------------------------------------------------------

%prep
%setup -q

#we do not introduce dependencies by example scripts.
chmod 644 EXAMPLES/*.pl 

%build
%configure  \
    --without-dyninst \
    --enable-sqlite \
    --disable-crash \
    --with-rpm \
    --disable-docs \
    --enable-pie \
    --without-java \
    --disable-virt \
    --with-python3

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}

# We want the examples in the special doc dir, not the build install dir.
# We build it in place and then move it away so it doesn't get installed
# twice. rpm can specify itself where the (versioned) docs go with the
# %doc directive.
mv $RPM_BUILD_ROOT%{_datadir}/doc/systemtap/examples examples

# Fix paths in the example & testsuite scripts
find examples testsuite -type f -name '*.stp' -print0 | xargs -0 sed -i -r -e '1s@^#!.+stap@#!%{_bindir}/stap@'

# To make rpmlint happy, remove any .gitignore files in the testsuite.
find testsuite -type f -name '.gitignore' -print0 | xargs -0 rm -f

# Because "make install" may install staprun with whatever mode, the
# post-processing programs rpmbuild runs won't be able to read it.
# So, we change permissions so that they can read it.  We'll set the
# permissions back to 04110 in the %files section below.
chmod 755 $RPM_BUILD_ROOT%{_bindir}/staprun

#install the useful stap-prep script
install -c -m 755 stap-prep $RPM_BUILD_ROOT%{_bindir}/stap-prep

# Copy over the testsuite
cp -rp testsuite $RPM_BUILD_ROOT%{_datadir}/systemtap

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/stap-server
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/stap-server
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/stap-server/.systemtap
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/stap-server
touch $RPM_BUILD_ROOT%{_localstatedir}/log/stap-server/log
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/systemtap
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/systemtap
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 initscript/logrotate.stap-server $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/stap-server
mkdir -p $RPM_BUILD_ROOT%{initdir}
install -m 755 initscript/systemtap $RPM_BUILD_ROOT%{initdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/script.d
install -m 644 initscript/config.systemtap $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/config

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
touch $RPM_BUILD_ROOT%{_unitdir}/stap-server.service
install -m 644 stap-server.service $RPM_BUILD_ROOT%{_unitdir}/stap-server.service
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 644 stap-server.conf $RPM_BUILD_ROOT%{_tmpfilesdir}/stap-server.conf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
install -p -m 644 emacs/systemtap-mode.el* $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -p -m 644 emacs/systemtap-init.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/systemtap-init.el


for subdir in ftdetect ftplugin indent syntax
do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/$subdir
    install -p -m 644 vim/$subdir/*.vim $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/$subdir
done


mkdir -p $RPM_BUILD_ROOT%{dracutstap}
install -p -m 755 initscript/99stap/module-setup.sh $RPM_BUILD_ROOT%{dracutstap}
install -p -m 755 initscript/99stap/start-staprun.sh $RPM_BUILD_ROOT%{dracutstap}
touch $RPM_BUILD_ROOT%{dracutstap}/params.conf

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre runtime
getent group stapusr >/dev/null || groupadd -g 156 -r stapusr 2>/dev/null || groupadd -r stapusr
getent group stapsys >/dev/null || groupadd -g 157 -r stapsys 2>/dev/null || groupadd -r stapsys
getent group stapdev >/dev/null || groupadd -g 158 -r stapdev 2>/dev/null || groupadd -r stapdev
exit 0

%pre server
getent group stap-server >/dev/null || groupadd -g 155 -r stap-server 2>/dev/null || groupadd -r stap-server
getent passwd stap-server >/dev/null || \
  useradd -c "Systemtap Compile Server" -u 155 -g stap-server -d %{_localstatedir}/lib/stap-server -r -s /sbin/nologin stap-server 2>/dev/null || \
  useradd -c "Systemtap Compile Server" -g stap-server -d %{_localstatedir}/lib/stap-server -r -s /sbin/nologin stap-server

%post server

# We have some duplication between the %files listings for the
# ~stap-server directories and the explicit mkdir/chown/chmod bits
# here.  Part of the reason may be that a preexisting stap-server
# account may well be placed somewhere other than
# %{_localstatedir}/lib/stap-server, but we'd like their permissions
# set similarly.

test -e ~stap-server && chmod 750 ~stap-server

if [ ! -f ~stap-server/.systemtap/rc ]; then
  mkdir -p ~stap-server/.systemtap
  chown stap-server:stap-server ~stap-server/.systemtap
  # PR16276: guess at a reasonable number for a default --rlimit-nproc
  numcpu=`/usr/bin/getconf _NPROCESSORS_ONLN`
  if [ -z "$numcpu" -o "$numcpu" -lt 1 ]; then numcpu=1; fi
  nproc=`expr $numcpu \* 30`
  echo "--rlimit-as=614400000 --rlimit-cpu=60 --rlimit-nproc=$nproc --rlimit-stack=1024000 --rlimit-fsize=51200000" > ~stap-server/.systemtap/rc
  chown stap-server:stap-server ~stap-server/.systemtap/rc
fi

test -e %{_localstatedir}/log/stap-server/log || {
     touch %{_localstatedir}/log/stap-server/log
     chmod 644 %{_localstatedir}/log/stap-server/log
     chown stap-server:stap-server %{_localstatedir}/log/stap-server/log
}
# If it does not already exist, as stap-server, generate the certificate
# used for signing and for ssl.
if test ! -e ~stap-server/.systemtap/ssl/server/stap.cert; then
   runuser -s /bin/sh - stap-server -c %{_libexecdir}/systemtap/stap-gen-cert >/dev/null
fi
# Prepare the service
     # Note, Fedora policy doesn't allow network services enabled by default
     # /bin/systemctl enable stap-server.service >/dev/null 2>&1 || :
     /bin/systemd-tmpfiles --create %{_tmpfilesdir}/stap-server.conf >/dev/null 2>&1 || :
exit 0

%triggerin client -- systemtap-server
if test -e ~stap-server/.systemtap/ssl/server/stap.cert; then
   # echo Authorizing ssl-peer/trusted-signer certificate for local systemtap-server
   %{_libexecdir}/systemtap/stap-authorize-cert ~stap-server/.systemtap/ssl/server/stap.cert %{_sysconfdir}/systemtap/ssl/client >/dev/null
   %{_libexecdir}/systemtap/stap-authorize-cert ~stap-server/.systemtap/ssl/server/stap.cert %{_sysconfdir}/systemtap/staprun >/dev/null
fi
exit 0
# XXX: corresponding %triggerun?

%preun server
# Check that this is the actual deinstallation of the package, as opposed to
# just removing the old package on upgrade.
if [ $1 = 0 ] ; then
       /bin/systemctl --no-reload disable stap-server.service >/dev/null 2>&1 || :
       /bin/systemctl stop stap-server.service >/dev/null 2>&1 || :
fi
exit 0

%postun server
# Check whether this is an upgrade of the package.
# If so, restart the service if it's running
if [ "$1" -ge "1" ] ; then
        /bin/systemctl condrestart stap-server.service >/dev/null 2>&1 || :
fi
exit 0

%post initscript
    /bin/systemctl enable systemtap.service >/dev/null 2>&1 || :
exit 0

%preun initscript
# Check that this is the actual deinstallation of the package, as opposed to
# just removing the old package on upgrade.
if [ $1 = 0 ] ; then
        /bin/systemctl --no-reload disable systemtap.service >/dev/null 2>&1 || :
        /bin/systemctl stop systemtap.service >/dev/null 2>&1 || :
fi
exit 0

%postun initscript
# Check whether this is an upgrade of the package.
# If so, restart the service if it's running
if [ "$1" -ge "1" ] ; then
        /bin/systemctl condrestart systemtap.service >/dev/null 2>&1 || :
fi
exit 0

%post
# Remove any previously-built uprobes.ko materials
(make -C %{_datadir}/systemtap/runtime/uprobes clean) >/dev/null 2>&1 || true
(/sbin/rmmod uprobes) >/dev/null 2>&1 || true

%preun
# Ditto
(make -C %{_datadir}/systemtap/runtime/uprobes clean) >/dev/null 2>&1 || true
(/sbin/rmmod uprobes) >/dev/null 2>&1 || true

# ------------------------------------------------------------------------

%files -f systemtap.lang
# The master "systemtap" rpm doesn't include any files.

%files server -f systemtap.lang
%defattr(-,root,root)
%{_bindir}/stap-server
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/stap-serverd
%{_libexecdir}/systemtap/stap-start-server
%{_libexecdir}/systemtap/stap-stop-server
%{_libexecdir}/systemtap/stap-gen-cert
%{_libexecdir}/systemtap/stap-sign-module
%{_libexecdir}/systemtap/stap-authorize-cert
%{_libexecdir}/systemtap/stap-env
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%{_mandir}/man8/stap-server.8*
%{_unitdir}/stap-server.service
%{_tmpfilesdir}/stap-server.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/stap-server
%dir %{_sysconfdir}/stap-server
%dir %attr(0750,stap-server,stap-server) %{_localstatedir}/lib/stap-server
%dir %attr(0700,stap-server,stap-server) %{_localstatedir}/lib/stap-server/.systemtap
%dir %attr(0755,stap-server,stap-server) %{_localstatedir}/log/stap-server
%ghost %config(noreplace) %attr(0644,stap-server,stap-server) %{_localstatedir}/log/stap-server/log
%ghost %attr(0755,stap-server,stap-server) %{_localstatedir}/run/stap-server
%doc README README.unprivileged AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING


%files devel -f systemtap.lang
%{_bindir}/stap
%{_bindir}/stap-prep
%{_bindir}/stap-report
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/runtime
%{_datadir}/systemtap/tapset
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%doc README README.unprivileged AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING

%{_datadir}/emacs/site-lisp/*.el*
%{_datadir}/emacs/site-lisp/site-start.d/systemtap-init.el
%{_datadir}/vim/vimfiles/*/*.vim


%files runtime -f systemtap.lang
%defattr(-,root,root)
%attr(4110,root,stapusr) %{_bindir}/staprun
%{_bindir}/stapsh
%{_bindir}/stap-merge
%{_bindir}/stap-report
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/stapio
%{_libexecdir}/systemtap/stap-authorize-cert

%{_mandir}/man1/stap-report.1*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/staprun.8*
%doc README README.security AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING


%files client -f systemtap.lang
%defattr(-,root,root)
%doc README README.unprivileged AUTHORS NEWS examples
%{!?_licensedir:%global license %%doc}
%license COPYING

%{_bindir}/stap
%{_bindir}/stap-prep
%{_bindir}/stap-report
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stap-merge.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man1/stapref.1*
%{_mandir}/man3/*
%{_mandir}/man7/error*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning*
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/tapset



%files initscript
%defattr(-,root,root)
%{initdir}/systemtap
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%config(noreplace) %{_sysconfdir}/systemtap/config
%dir %{_localstatedir}/cache/systemtap
%ghost %{_localstatedir}/run/systemtap
%{_mandir}/man8/systemtap.8*
   %dir %{dracutstap}
   %{dracutstap}/*


%files sdt-devel
%defattr(-,root,root)
%{_bindir}/dtrace
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_mandir}/man1/dtrace.1*
%doc README AUTHORS NEWS 
%{!?_licensedir:%global license %%doc}
%license COPYING


%files testsuite
%defattr(-,root,root)
%dir %{_datadir}/systemtap
%{_datadir}/systemtap/testsuite


# ------------------------------------------------------------------------
%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 3.0-0.20151027git8136768
- Initial build

