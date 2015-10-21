Summary:    Firmware extraction tools for Apple Built-in iSight camera
Name:       isight-firmware-tools
Version:    1.6
Release:    9
License:    GPLv2+
Group:      System Environment/Base
URL:        http://launchpad.net/isight-firmware-tools/
Source0:    http://launchpad.net/isight-firmware-tools/main/1.6/+download/%{name}-%{version}.tar.gz
Patch0:     isight-firmware-tools-ift-load-path.patch
Patch1:     isight-firmware-tools-1.6-formatsecurity.patch

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:   udev

BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libusb-devel
BuildRequires:  perl(XML::Parser)
BuildRequires:  intltool

%description
iSight Firmware Tools provide tools to manipulate firmware for Built-in iSight
cameras found on Apple machines since iMac G5 (November 2005).

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .formatsecurity
%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot} 

make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_infodir}

# Use doc instead.
rm -rf %{buildroot}%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%config %{_sysconfdir}/udev/rules.d/isight.rules
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc HOWTO
%doc NEWS
%doc README
%{_bindir}/ift-export
%{_bindir}/ift-extract
%{_mandir}/man1/ift-export.1.gz
%{_mandir}/man1/ift-extract.1.gz
/lib/udev/ift-load

%changelog
* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
