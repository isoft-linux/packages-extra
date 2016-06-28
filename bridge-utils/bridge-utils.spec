Summary:        Utilities for configuring the linux ethernet bridge
Name:           bridge-utils
Version:        1.5
Release:        13
License:        GPLv2+
URL:            http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Group:          System Environment/Base

Source:         http://downloads.sourceforge.net/bridge/%{name}-%{version}.tar.gz
Patch0:         bridge-utils-1.5-fix-incorrect-command-in-manual.patch
Patch1:         bridge-utils-1.5-fix-error-message-for-incorrect-command.patch
Patch2:         bridge-utils-1.5-check-error-returns-from-write-to-sysfs.patch
Patch10:        bridge-utils-1.0.4-inc.patch
Patch11:        bridge-utils-1.5-linux_3.8.x.patch
Patch12:        bridge-utils-libbridge-cflags.patch

BuildRequires:  libsysfs-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  kernel-headers >= 2.6.16

%description
This package contains utilities for configuring the linux ethernet
bridge. The linux ethernet bridge can be used for connecting multiple
ethernet devices together. The connecting is fully transparent: hosts
connected to one ethernet device see hosts connected to the other
ethernet devices directly.

Install bridge-utils if you want to use the linux ethernet bridge.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1 -b libbridge

%build
autoconf
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} SUBDIRS="brctl doc" install

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS doc/FAQ doc/HOWTO
%{_sbindir}/brctl
%{_mandir}/man8/brctl.8*

%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.5-13
- rebuilt for libvirt

