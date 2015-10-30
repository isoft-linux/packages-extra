Summary: A network traffic monitoring tool
Name: tcpdump
Version: 4.7.4
Release: 4
License: BSD
URL: http://www.tcpdump.org
Requires(pre): shadow-utils 
BuildRequires: openssl-devel

Source0: http://www.tcpdump.org/release/tcpdump-%{version}.tar.gz

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%prep
%setup -q 
%build
%configure --with-user=tcpdump
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 tcpdump ${RPM_BUILD_ROOT}%{_sbindir}
install -m644 tcpdump.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdump.8

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
/usr/sbin/groupadd -g 72 tcpdump 2> /dev/null
/usr/sbin/useradd -u 72 -g 72 -s /sbin/nologin -M -r \
	-d / tcpdump 2> /dev/null
exit 0

%files
%defattr(-,root,root)
%{_sbindir}/tcpdump
%{_mandir}/man8/tcpdump.8*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.7.4-4
- Rebuild

