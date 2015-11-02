#TODO: stop using local copy of libdnet, once system distributed version supports sctp (grep sctp /usr/include/dnet.h)
Summary: Network exploration tool and security scanner
Name: nmap
Epoch: 2
Version: 6.47
#global prerelease TEST5
Release: 6%{?dist}
# Uses combination of licenses based on GPL license, but with extra modification
# so it got its own license tag rhbz#1055861
License: Nmap
Requires: %{name}-ncat = %{epoch}:%{version}-%{release}
Source0: http://nmap.org/dist/%{name}-%{version}%{?prerelease}.tar.bz2
Source1: zenmap.desktop
Source2: zenmap-root.pamd
Source3: zenmap-root.consoleapps

#prevent possible race condition for shtool, rhbz#158996
Patch1: nmap-4.03-mktemp.patch

#don't suggest to scan microsoft
Patch2: nmap-4.52-noms.patch

# upstream provided patch for rhbz#845005, not yet in upstream repository
Patch5: ncat_reg_stdin.diff
Patch6: nmap-6.25-displayerror.patch

#rhbz#994376
Patch7: nmap-6.40-logdebug.patch
#sent upstream, rhbz#978964
Patch8: nmap-6.40-allresolve.patch

URL: http://nmap.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, gtk2-devel, lua-devel, libpcap-devel, pcre-devel
BuildRequires: desktop-file-utils, dos2unix
BuildRequires: libtool, automake, autoconf, gettext-devel

%define pixmap_srcdir zenmap/share/pixmaps

%description
Nmap is a utility for network exploration or security auditing.  It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, reverse-identd scanning, and more. In addition
to the classic command-line nmap executable, the Nmap suite includes a flexible
data transfer, redirection, and debugging tool (netcat utility ncat), a utility
for comparing scan results (ndiff), and a packet generation and response analysis
tool (nping). 

%package frontend
Summary: The GTK+ front end for nmap
Requires: nmap = %{epoch}:%{version} gtk2 python >= 2.5 pygtk2 usermode
BuildRequires: python >= 2.5 python-devel pygtk2-devel libpng-devel
BuildArch: noarch
%description frontend
This package includes zenmap, a GTK+ front end for nmap. The nmap package must
be installed before installing nmap front end.

%package ncat
Summary: Nmap's Netcat replacement
Obsoletes: nc < 1.109.20120711-2
Provides: nc
%description ncat
Ncat is a feature packed networking utility which will read and
write data across a network from the command line.  It uses both
TCP and UDP for communication and is designed to be a reliable
back-end tool to instantly provide network connectivity to other
applications and users. Ncat will not only work with IPv4 and IPv6
but provides the user with a virtually limitless number of potential
uses.


%prep
%setup -q -n %{name}-%{version}%{?prerelease}
%patch1 -p1 -b .mktemp
%patch2 -p1 -b .noms
%patch5 -p1 -b .ncat_reg_stdin
%patch6 -p1 -b .displayerror
%patch7 -p1 -b .logdebug
%patch8 -p1 -b .allresolve

# for aarch64 support, not needed with autotools 2.69+
for f in acinclude.m4 configure.ac nping/configure.ac
do
  sed -i -e 's/\(AC_DEFINE([^,)]*\))/\1, 1, [Description])/' -e 's/\(AC_DEFINE([^,]*,[^,)]*\))/\1, [Description])/' $f
done
autoreconf -I . -fiv --no-recursive
cd nping; autoreconf -I .. -fiv --no-recursive; cd ..

#be sure we're not using tarballed copies of some libraries
#rm -rf liblua libpcap libpcre macosx mswin32 ###TODO###
rm -rf libpcap libpcre macosx mswin32

#fix locale dir
mv zenmap/share/zenmap/locale zenmap/share
sed -i -e "s|^locale_dir =.*$|locale_dir = os.path.join('share','locale')|" \
 -e 's|join(self.install_data, data_dir)|join(self.install_data, "share")|' zenmap/setup.py
sed -i 's|^LOCALE_DIR = .*|LOCALE_DIR = join(prefix, "share", "locale")|' zenmap/zenmapCore/Paths.py

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
#%configure  --with-libpcap=/usr ###TODO###
%configure  --with-libpcap=/usr --with-liblua=included
make %{?_smp_mflags}

#fix man page (rhbz#813734)
sed -i 's/-md/-mf/' nping/docs/nping.1

%install
rm -rf $RPM_BUILD_ROOT

#prevent stripping - replace strip command with 'true'
make DESTDIR=$RPM_BUILD_ROOT STRIP=true install
rm -f $RPM_BUILD_ROOT%{_bindir}/uninstall_zenmap

#do not include certificate bundle (#734389)
rm -f $RPM_BUILD_ROOT%{_datadir}/ncat/ca-bundle.crt
rmdir $RPM_BUILD_ROOT%{_datadir}/ncat

#use consolehelper
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/zenmap*.desktop
rm -f $RPM_BUILD_ROOT%{_datadir}/zenmap/su-to-zenmap.sh
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/zenmap-root
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/zenmap-root
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/zenmap-root

cp docs/zenmap.1 $RPM_BUILD_ROOT%{_mandir}/man1/
gzip $RPM_BUILD_ROOT%{_mandir}/man1/* || :
pushd $RPM_BUILD_ROOT%{_mandir}/man1
ln -s zenmap.1.gz nmapfe.1.gz
ln -s zenmap.1.gz xnmap.1.gz
popd

#we provide 'nc' replacement
ln -s ncat.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/nc.1.gz
ln -s ncat $RPM_BUILD_ROOT%{_bindir}/nc

desktop-file-install --vendor nmap \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--add-category X-Red-Hat-Base \
	%{SOURCE1};

#for .desktop and app icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
ln -s ../../../../zenmap/pixmaps/zenmap.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps

# fix end-of-line
pushd $RPM_BUILD_ROOT
for fe in ./%{python_sitelib}/zenmapCore/Paths.py
do
  dos2unix <$fe >$fe.new
  touch -r $fe $fe.new
  mv -f $fe.new $fe
done
popd

%find_lang nmap --with-man
%find_lang zenmap

%post frontend
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun frontend
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans frontend
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files -f nmap.lang
%defattr(-,root,root)
%doc COPYING*
%doc docs/README
%doc docs/nmap.usage.txt
%{_bindir}/nmap
%{_bindir}/ndiff
%{_bindir}/nping
%{_mandir}/man1/ndiff.1.gz
%{_mandir}/man1/nmap.1.gz
%{_mandir}/man1/nping.1.gz
%{_datadir}/nmap

%files ncat 
%defattr(-,root,root)
%doc COPYING ncat/docs/AUTHORS ncat/docs/README ncat/docs/THANKS ncat/docs/examples
%{_bindir}/nc
%{_bindir}/ncat
%{_mandir}/man1/nc.1.gz
%{_mandir}/man1/ncat.1.gz

%files frontend -f zenmap.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/zenmap-root
%config(noreplace) %{_sysconfdir}/security/console.apps/zenmap-root
%{_bindir}/zenmap-root
%{_bindir}/zenmap
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{python_sitelib}/*
%{_datadir}/applications/nmap-zenmap.desktop
%{_datadir}/icons/hicolor/256x256/apps/*
%{_datadir}/zenmap
%{_mandir}/man1/zenmap.1.gz
%{_mandir}/man1/nmapfe.1.gz
%{_mandir}/man1/xnmap.1.gz

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 2:6.47-6
- Initial build


