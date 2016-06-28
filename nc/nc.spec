Summary:    Reads and writes data across network connections using TCP or UDP
Name:       nc
# CVS version of netcat.c + the checkout date
Version:    1.109.20120711
Release:    2%{?dist}
URL:        http://www.openbsd.org/cgi-bin/cvsweb/src/usr.bin/%{name}/
License:    BSD and ISC
Group:      Applications/Internet
# source is CVS checkout, e.g.:
# CVSROOT=anoncvs@anoncvs.openbsd.org.ar:/cvs/src/usr.bin cvs checkout nc
Source0:    %{name}-%{version}.tar.bz2
Patch0:     nc-1.107-linux-ify.patch
Patch1:     nc-1.107-pollhup.patch
Patch2:     nc-1.107-udp-stop.patch
Patch3:     nc-1.107-udp-portscan.patch
Patch4:     nc-1.107-crlf.patch
Patch5:     nc-1.107-comma.patch
Patch6:     nc-1.100-libbsd.patch
Patch7:     nc-1.107-initialize-range.patch
Patch8:     nc-1.107-iptos-class.patch

BuildRequires: libbsd-devel

%description
The nc package contains Netcat (the program is actually nc), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols. Netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  Netcat is also a feature-rich network debugging and
exploration tool, since it can create many different connections and
has many built-in capabilities.

You may want to install the netcat package if you are administering a
network and you'd like to use its debugging and network exploration
capabilities.

%prep
%setup -q -n nc
%patch0 -p1 -b .linux-ify
%patch1 -p1 -b .pollhup
%patch2 -p1 -b .udp-stop
%patch3 -p1 -b .udp-portscan
%patch4 -p1 -b .crlf
%patch5 -p1 -b .comma
%patch6 -p1 -b .libbsd
%patch7 -p1 -b .initialize-range
%patch8 -p1 -b .iptos-class

%build
gcc %{optflags} -lresolv `pkg-config --cflags --libs libbsd` -o nc netcat.c atomicio.c socks.c

%install
install -d %{buildroot}%{_bindir}
install -m755 -p nc %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -m644 -p nc.1 %{buildroot}%{_mandir}/man1

%files
%{_bindir}/nc
%{_mandir}/man1/nc.1*

%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.109.20120711-2
- rebuilt for libvirt

