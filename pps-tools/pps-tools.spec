Name:		pps-tools
Version:	0
Release:	0.12.20120407git0deb9c%{?dist}
Summary:	LinuxPPS user-space tools

License:	GPLv2+
URL:		https://github.com/ago/pps-tools

# git clone git://github.com/ago/pps-tools; cd pps-tools
# git archive --prefix=pps-tools/ 0deb9c | xz > pps-tools-20120407git0deb9c.tar.xz
Source0:	pps-tools-20120407git0deb9c.tar.xz

%description
This package includes the LinuxPPS user-space tools.

%package devel
Summary: LinuxPPS PPSAPI header file

%description devel
This package includes the header needed to compile PPSAPI (RFC-2783)
applications.

%prep
%setup -q -n %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} 

%install
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/sys}
install -m755 -t $RPM_BUILD_ROOT%{_bindir} ppsctl ppsfind ppstest ppswatch
install -p -m644 -t $RPM_BUILD_ROOT%{_includedir}/sys timepps.h

%files
%doc COPYING debian/README debian/copyright
%{_bindir}/pps*

%files devel
%doc COPYING debian/copyright
%{_includedir}/sys/timepps.h

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0-0.12.20120407git0deb9c
- Rebuild

