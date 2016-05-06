Name:           netcf
Version:        0.2.8
Release:        4%{?dist}%{?extra_release}
Summary:        Cross-platform network configuration library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://fedorahosted.org/netcf/
Source0:        https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches
# One patch per line, in this format:
# Patch001: file1.patch
# Patch002: file2.patch
# ...
#
# The patches will automatically be put into the build source tree
# during the %prep stage (using git, which is now required for an rpm
# build)
#
Patch001: netcf-call-aug_load-at-most-once-per-second.patch
Patch002: netcf-optimize-aug_match-query-for-all-ifcfg-files-related.patch
Patch003: netcf-linux-include-bond-element-for-bonds-with-no-slaves.patch 
Patch004: netcf-Properly-classify-bond-devices-with-no-slaves.patch 

# Default to skipping autoreconf.  Distros can change just this one
# line (or provide a command-line override) if they backport any
# patches that touch configure.ac or Makefile.am.
%{!?enable_autotools:%define enable_autotools 0}

# git is used to build a source tree with patches applied (see the
# %prep section)
BuildRequires: git

# Fedora 20 / RHEL-7 are where netcf first uses systemd. Although earlier
# Fedora has systemd, netcf still used sysvinit there.
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
    %define with_systemd 1
%else
    %define with_systemd 1
%endif

%if %{with_systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: /usr/bin/pod2man
%endif

BuildRequires:  readline-devel augeas-devel >= 0.5.2
BuildRequires:  libxml2-devel libxslt-devel

# force the --with-libnl1 option on F17/RHEL6 and earlier
%if (0%{?fedora} && 0%{?fedora} < 18) || (0%{?rhel} && 0%{?rhel} < 7)
%define with_libnl1 1
%else
%define with_libnl1 0
%endif

# require libnl3 on F18/RHEL7 and later
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires:  libnl3-devel
%else
BuildRequires:  libnl-devel
%endif

Requires:       %{name}-libs = %{version}-%{release}

Provides: bundled(gnulib)

%description
Netcf is a library used to modify the network configuration of a
system. Network configurations are expressed in a platform-independent
XML format, which netcf translates into changes to the system's
'native' network configuration files.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

# bridge-utils is needed because /sbin/ifup calls brctl
# if you create a bridge device
Requires:       bridge-utils

%description    libs
The libraries for %{name}.

%prep
%setup -q

# Patches have to be stored in a temporary file because RPM has
# a limit on the length of the result of any macro expansion;
# if the string is longer, it's silently cropped
%{lua:
    tmp = os.tmpname();
    f = io.open(tmp, "w+");
    count = 0;
    for i, p in ipairs(patches) do
        f:write(p.."\n");
        count = count + 1;
    end;
    f:close();
    print("PATCHCOUNT="..count.."\n")
    print("PATCHLIST="..tmp.."\n")
}

git init -q
git config user.name rpm-build
git config user.email rpm-build
git config gc.auto 0
git add .
git commit -q -a --author 'rpm-build <rpm-build>' \
           -m '%{name}-%{version} base'

COUNT=$(grep '\.patch$' $PATCHLIST | wc -l)
if [ $COUNT -ne $PATCHCOUNT ]; then
    echo "Found $COUNT patches in $PATCHLIST, expected $PATCHCOUNT"
    exit 1
fi
if [ $COUNT -gt 0 ]; then
    xargs git am <$PATCHLIST || exit 1
fi
echo "Applied $COUNT patches"
rm -f $PATCHLIST


%build
%if %{with_libnl1}
%define _with_libnl1 --with-libnl1
%endif
%if %{with_systemd}
    %define sysinit --with-sysinit=systemd
%else
    %define sysinit --with-sysinit=initscripts
%endif


%if 0%{?enable_autotools}
 autoreconf -if
%endif

%configure --disable-static \
           %{?_with_libnl1} \
           %{sysinit} \
            --with-driver=redhat
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT SYSTEMD_UNIT_DIR=%{_unitdir} \
     INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -delete

%preun libs

%if %{with_systemd}
    %systemd_preun netcf-transaction.service
%else
if [ $1 = 0 ]; then
    /sbin/chkconfig --del netcf-transaction
fi
%endif

%post libs

/sbin/ldconfig
%if %{with_systemd}
    %systemd_post netcf-transaction.service
    /bin/systemctl --no-reload enable netcf-transaction.service >/dev/null 2>&1 || :
%else
/sbin/chkconfig --add netcf-transaction
%endif

%postun libs

/sbin/ldconfig
%if %{with_systemd}
    %systemd_postun netcf-transaction.service
%endif

%files
%{_bindir}/ncftool
%{_mandir}/man1/ncftool.1*

%files libs
%{_datadir}/netcf
%{_libdir}/*.so.*
%if %{with_systemd}
%{_unitdir}/netcf-transaction.service
%else
%{_sysconfdir}/rc.d/init.d/netcf-transaction
%endif
%attr(0755, root, root) %{_libexecdir}/netcf-transaction.sh
%doc AUTHORS COPYING NEWS

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcf.pc

%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 0.2.8-4
- rebuilt for libvirt,add:--with-driver=redhat

