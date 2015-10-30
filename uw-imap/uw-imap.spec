%define _with_devel 1
# ship static lib, matches default upstream config
# as convenience to users, since our hacked shlib can potentially break 
# abi semi-often
%define _with_static 1

%define _with_system_libc_client 0 

Summary: UW Server daemons for IMAP and POP network mail protocols
Name:	 uw-imap 
Version: 2007f
Release: 11%{?dist}

# See LICENSE.txt, http://www.apache.org/licenses/LICENSE-2.0
License: ASL 2.0 
URL:	 http://www.washington.edu/imap/
# Old (non-latest) releases live at  ftp://ftp.cac.washington.edu/imap/old/
Source0: ftp://ftp.cac.washington.edu/imap/imap-%{version}%{?beta}%{?dev}%{?snap}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define soname    c-client
#define somajor   %{version} 
%define somajor   2007
%define shlibname lib%{soname}.so.%{somajor}
%define imap_libs lib%{soname}

# FC4+ uses %%_sysconfdir/pki/tls, previous releases used %%_datadir/ssl
%global ssldir  %(if [ -d %{_sysconfdir}/pki/tls ]; then echo "%{_sysconfdir}/pki/tls"; else echo "%{_datadir}/ssl"; fi)

# imap -> uw-imap rename
Obsoletes: imap < 1:%{version}

# newest pam setup, using password-auth common PAM
Source20: imap-password.pam

Source31: imap-xinetd
Source32: imaps-xinetd
Source33: ipop2-xinetd
Source34: ipop3-xinetd
Source35: pop3s-xinetd

Patch1: imap-2007-paths.patch
# See http://bugzilla.redhat.com/229781 , http://bugzilla.redhat.com/127271
Patch2: imap-2004a-doc.patch
Patch5: imap-2007e-overflow.patch
Patch9: imap-2007e-shared.patch
Patch10: imap-2007e-authmd5.patch
Patch11: imap-2007e-system_c_client.patch
Patch12: imap-2007f-format-security.patch

BuildRequires: krb5-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel

Requires: xinetd
Requires(post): openssl

%if 0%{?_with_system_libc_client}
BuildRequires: libc-client-devel = %{version}
Requires: %{imap_libs}%{?_isa} = %{version}
%else
Requires: %{imap_libs}%{?_isa} = %{version}-%{release}
%endif

%description
The %{name} package provides UW server daemons for both the IMAP (Internet
Message Access Protocol) and POP (Post Office Protocol) mail access
protocols.  The POP protocol uses a "post office" machine to collect
mail for users and allows users to download their mail to their local
machine for reading. The IMAP protocol allows a user to read mail on a
remote machine without downloading it to their local machine.

%package -n %{imap_libs} 
Summary: UW C-client mail library 
Obsoletes: libc-client2004d < 1:2004d-2
Obsoletes: libc-client2004e < 2004e-2
Obsoletes: libc-client2004g < 2004g-7
Obsoletes: libc-client2006 < 2006k-2
%if "%{imap_libs}" != "libc-client2007"
Obsoletes: libc-client2007 < 2007-2
%endif
%description -n %{imap_libs} 
Provides a common API for accessing mailboxes. 

%package devel
Summary: Development tools for programs which will use the UW IMAP library
Requires: %{imap_libs}%{?_isa} = %{version}-%{release}
# imap -> uw-imap rename
Obsoletes: imap-devel < 1:%{version}
%if "%{imap_libs}" == "libc-client"
Obsoletes: libc-client-devel < %{version}-%{release}
Provides:  libc-client-devel = %{version}-%{release}
%else
Conflicts: libc-client-devel < %{version}-%{release}
%endif
%description devel
Contains the header files and libraries for developing programs 
which will use the UW C-client common API.

%package static 
Summary: UW IMAP static library
Requires: %{name}-devel = %{version}-%{release}
#Provides: libc-client-static = %{version}-%{release}
Requires: krb5-devel openssl-devel pam-devel
%description static 
Contains static libraries for developing programs 
which will use the UW C-client common API.

%package utils
Summary: UW IMAP Utilities to make managing your email simpler
%if ! 0%{?_with_system_libc_client}
Requires: %{imap_libs}%{?_isa} = %{version}-%{release}
%endif
# imap -> uw-imap rename
Obsoletes: imap-utils < 1:%{version}
%description utils
This package contains some utilities for managing UW IMAP email,including:
* dmail : procmail Mail Delivery Module
* mailutil : mail utility program
* mtest : C client test program
* tmail : Mail Delivery Module
* mlock



%prep
%setup -q -n imap-%{version}%{?dev}%{?snap}

%patch1 -p1 -b .paths
%patch2 -p1 -b .doc

%patch5 -p1 -b .overflow

%patch9 -p1 -b .shared
%patch10 -p1 -b .authmd5

install -p -m644 %{SOURCE20} imap.pam

%if 0%{?_with_system_libc_client}
%patch11 -p1 -b .system_c_client
%endif

%patch12 -p1 -b .fmt-sec


%build

# Kerberos setup
test -f %{_sysconfdir}/profile.d/krb5-devel.sh && source %{_sysconfdir}/profile.d/krb5-devel.sh
test -f %{_sysconfdir}/profile.d/krb5.sh && source %{_sysconfdir}/profile.d/krb5.sh
GSSDIR=$(krb5-config --prefix)

# SSL setup, probably legacy-only, but shouldn't hurt -- Rex
export EXTRACFLAGS="$EXTRACFLAGS $(pkg-config --cflags openssl 2>/dev/null)"
# $RPM_OPT_FLAGS
export EXTRACFLAGS="$EXTRACFLAGS -fPIC $RPM_OPT_FLAGS"
# jorton added these, I'll assume he knows what he's doing. :) -- Rex
export EXTRACFLAGS="$EXTRACFLAGS -fno-strict-aliasing"
export EXTRACFLAGS="$EXTRACFLAGS -Wno-pointer-sign"

echo -e "y\ny" | \
make %{?_smp_mflags} lnp \
IP=6 \
EXTRACFLAGS="$EXTRACFLAGS" \
EXTRALDFLAGS="$EXTRALDFLAGS" \
EXTRAAUTHENTICATORS=gss \
SPECIALS="GSSDIR=${GSSDIR} LOCKPGM=%{_sbindir}/mlock SSLCERTS=%{ssldir}/certs SSLDIR=%{ssldir} SSLINCLUDE=%{_includedir}/openssl SSLKEYS=%{ssldir}/private SSLLIB=%{_libdir}" \
SSLTYPE=unix \
%if 0%{?_with_system_libc_client}
CCLIENTLIB=%{_libdir}/%{shlibname} \
%else
CCLIENTLIB=$(pwd)/c-client/%{shlibname} \
%endif
SHLIBBASE=%{soname} \
SHLIBNAME=%{shlibname} \
%if 0%{?_with_system_libc_client}
%endif
# Blank line


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/

%if ! 0%{?_with_system_libc_client}
%if 0%{?_with_static:1}
install -p -m644 ./c-client/c-client.a $RPM_BUILD_ROOT%{_libdir}/
ln -s c-client.a $RPM_BUILD_ROOT%{_libdir}/libc-client.a
%endif

install -p -m755 ./c-client/%{shlibname} $RPM_BUILD_ROOT%{_libdir}/

# %%ghost'd c-client.cf
touch c-client.cf
install -p -m644 -D c-client.cf $RPM_BUILD_ROOT%{_sysconfdir}/c-client.cf
%endif

%if 0%{?_with_devel:1}
ln -s %{shlibname} $RPM_BUILD_ROOT%{_libdir}/lib%{soname}.so

mkdir -p $RPM_BUILD_ROOT%{_includedir}/imap/
install -m644 ./c-client/*.h $RPM_BUILD_ROOT%{_includedir}/imap/
# Added linkage.c to fix (#34658) <mharris>
install -m644 ./c-client/linkage.c $RPM_BUILD_ROOT%{_includedir}/imap/
install -m644 ./src/osdep/tops-20/shortsym.h $RPM_BUILD_ROOT%{_includedir}/imap/
%endif

install -p -D -m644 src/imapd/imapd.8 $RPM_BUILD_ROOT%{_mandir}/man8/imapd.8uw
install -p -D -m644 src/ipopd/ipopd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ipopd.8uw

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -p -m755 ipopd/ipop{2d,3d} $RPM_BUILD_ROOT%{_sbindir}/
install -p -m755 imapd/imapd $RPM_BUILD_ROOT%{_sbindir}/
install -p -m755 mlock/mlock $RPM_BUILD_ROOT%{_sbindir}/

mkdir -p $RPM_BUILD_ROOT%{_bindir}/
install -p -m755 dmail/dmail mailutil/mailutil mtest/mtest tmail/tmail $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m644 src/{dmail/dmail,mailutil/mailutil,tmail/tmail}.1 $RPM_BUILD_ROOT%{_mandir}/man1/

install -p -m644 -D imap.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/imap
install -p -m644 -D imap.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/pop

install -p -m644 -D %{SOURCE31} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/imap
install -p -m644 -D %{SOURCE32} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/imaps
install -p -m644 -D %{SOURCE33} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/ipop2
install -p -m644 -D %{SOURCE34} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/ipop3
install -p -m644 -D %{SOURCE35} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/pop3s

# %ghost'd *.pem files
mkdir -p $RPM_BUILD_ROOT%{ssldir}/certs
touch $RPM_BUILD_ROOT%{ssldir}/certs/{imapd,ipop3d}.pem


%clean
rm -rf $RPM_BUILD_ROOT


# FIXME, do on first launch (or not at all?), not here -- Rex
%post
{
cd %{ssldir}/certs &> /dev/null || :
for CERT in imapd.pem ipop3d.pem ;do
   if [ ! -e $CERT ];then
      if [ -e stunnel.pem ];then
         cp stunnel.pem $CERT &> /dev/null || :
      elif [ -e Makefile ];then
         make $CERT << EOF &> /dev/null || :
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
      fi
   fi
done
} || :
/sbin/service xinetd reload > /dev/null 2>&1 || :

%postun
/sbin/service xinetd reload > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc docs/SSLBUILD
%config(noreplace) %{_sysconfdir}/pam.d/imap
%config(noreplace) %{_sysconfdir}/pam.d/pop
%config(noreplace) %{_sysconfdir}/xinetd.d/imap
%config(noreplace) %{_sysconfdir}/xinetd.d/ipop2
%config(noreplace) %{_sysconfdir}/xinetd.d/ipop3
# These need to be replaced (ie, can't use %%noreplace), or imaps/pop3s can fail on upgrade
# do this in a %trigger or something not here... -- Rex
%config(noreplace) %{_sysconfdir}/xinetd.d/imaps
%config(noreplace) %{_sysconfdir}/xinetd.d/pop3s
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/certs/imapd.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/certs/ipop3d.pem
%{_mandir}/man8/*
%{_sbindir}/ipop2d
%{_sbindir}/ipop3d
%{_sbindir}/imapd

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%attr(2755, root, mail) %{_sbindir}/mlock
%{_mandir}/man1/*

%if ! 0%{?_with_system_libc_client}
%post -n %{imap_libs} -p /sbin/ldconfig
%postun -n %{imap_libs} -p /sbin/ldconfig

%files -n %{imap_libs} 
%defattr(-,root,root)
%doc LICENSE.txt NOTICE SUPPORT 
%doc docs/RELNOTES docs/*.txt
%ghost %config(missingok,noreplace) %{_sysconfdir}/c-client.cf
%{_libdir}/lib%{soname}.so.*
%endif

%if 0%{?_with_devel:1}
%files devel
%defattr(-,root,root,-)
%{_includedir}/imap/
%{_libdir}/lib%{soname}.so
%endif

%if 0%{?_with_static:1}
%files static
%defattr(-,root,root,-)
%{_libdir}/c-client.a
%{_libdir}/libc-client.a
%endif


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2007f-11
- Initial build

