# -*- rpm-spec -*-


%define with_guestfs               0
%define stable_defaults            0
%define askpass_package            "openssh-askpass"
%define qemu_user                  "qemu"
%define libvirt_packages           "libvirt-daemon-kvm,libvirt-daemon-config-network"
%define kvm_packages               ""
%define preferred_distros          "isoft,fedora,rhel"
%define default_hvs                "qemu,xen,lxc"

%if 0%{?rhel}
%define preferred_distros          "rhel,fedora,isoft"
%define stable_defaults            1
%endif


# End local config

Name: virt-manager
Version: 1.3.2
Release: 2%{?dist}
%define verrel %{version}-%{release}

Summary: Desktop tool for managing virtual machines via libvirt
License: GPLv2+
URL: http://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz

# Fix screenshot on F24 rawhide (bz #1297988)
Patch0001: 0001-details-Fix-screenshot-on-F24-rawhide-bz-1297988.patch
# Fix URL installs when content-length header missing (bz #1297900)
Patch0002: 0002-urlfetcher-Fix-URL-installs-when-content-length-head.patch
BuildArch: noarch


Requires: virt-manager-common = %{verrel}
Requires: pygobject3
Requires: gtk3
Requires: libvirt-glib >= 0.0.9
Requires: python-libxml2
Requires: dconf
Requires: dbus-x11

# The vte291 package is actually the latest vte with API version 2.91, while
# the vte3 package is effectively a compat package with API version 2.90.
# virt-manager works fine with either, so pull the latest bits so there's
# no ambiguity.
Requires: vte3

# For console widget
Requires: gtk-vnc
Requires: spice-gtk

%if 0%{?rhel} == 7
Requires: gnome-icon-theme
%endif


BuildRequires: python
BuildRequires: intltool
BuildRequires: /usr/bin/pod2man
BuildRequires: glib2


%description
Virtual Machine Manager provides a graphical tool for administering virtual
machines for KVM, Xen, and LXC. Start, stop, add or remove virtual devices,
connect to a graphical or serial console, and see resource usage statistics
for existing VMs on local or remote machines. Uses libvirt as the backend
management API.


%package common
Summary: Common files used by the different Virtual Machine Manager interfaces

# This version not strictly required: virt-manager should work with older,
# however varying amounts of functionality will not be enabled.
Requires: libvirt-python >= 0.7.0
Requires: python-libxml2
Requires: python-requests
Requires: python-ipaddr
#Requires: libosinfo >= 0.2.10
# Required for gobject-introspection infrastructure
Requires: pygobject3-base

%description common
Common files used by the different virt-manager interfaces, as well as
virt-install related tools.


%package -n virt-install
Summary: Utilities for installing virtual machines

Requires: virt-manager-common = %{verrel}

Provides: virt-install
Provides: virt-clone
Provides: virt-convert
Provides: virt-xml
Obsoletes: python-virtinst

%description -n virt-install
Package includes several command line utilities, including virt-install
(build and install new VMs) and virt-clone (clone an existing virtual
machine).


%prep
%setup -q

# Fix screenshot on F24 rawhide (bz #1297988)
%patch0001 -p1
# Fix URL installs when content-length header missing (bz #1297900)
%patch0002 -p1

%build
%if %{qemu_user}
%define _qemu_user --qemu-user=%{qemu_user}
%endif

%if %{kvm_packages}
%define _kvm_packages --kvm-package-names=%{kvm_packages}
%endif

%if %{preferred_distros}
%define _preferred_distros --preferred-distros=%{preferred_distros}
%endif

%if %{libvirt_packages}
%define _libvirt_packages --libvirt-package-names=%{libvirt_packages}
%endif

%if %{askpass_package}
%define _askpass_package --askpass-package-names=%{askpass_package}
%endif

%if %{stable_defaults}
%define _stable_defaults --stable-defaults
%endif

%if %{default_hvs}
%define _default_hvs --default-hvs %{default_hvs}
%endif

python setup.py configure \
    %{?_qemu_user} \
    %{?_kvm_packages} \
    %{?_libvirt_packages} \
    %{?_askpass_package} \
    %{?_preferred_distros} \
    %{?_stable_defaults} \
    %{?_default_hvs}


%install
python setup.py \
    --no-update-icon-cache --no-compile-schemas \
    install -O1 --root=%{buildroot}
%find_lang %{name}

# The conversion script was only added to virt-manager after several
# Fedora cycles of using gsettings. Installing it now could convert old data
# and wipe out recent settings.
rm %{buildroot}%{_datadir}/GConf/gsettings/org.virt-manager.virt-manager.convert


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc README COPYING NEWS
%{_bindir}/%{name}

%{_mandir}/man1/%{name}.1*

%{_datadir}/%{name}/ui/*.ui
%{_datadir}/%{name}/virt-manager
%{_datadir}/%{name}/virtManager

%{_datadir}/%{name}/icons
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml


%files common -f %{name}.lang
%dir %{_datadir}/%{name}

%{_datadir}/%{name}/virtcli
%{_datadir}/%{name}/virtconv
%{_datadir}/%{name}/virtinst


%files -n virt-install
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-clone.1*
%{_mandir}/man1/virt-convert.1*
%{_mandir}/man1/virt-xml.1*

%{_datadir}/%{name}/virt-install
%{_datadir}/%{name}/virt-clone
%{_datadir}/%{name}/virt-convert
%{_datadir}/%{name}/virt-xml

%{_bindir}/virt-install
%{_bindir}/virt-clone
%{_bindir}/virt-convert
%{_bindir}/virt-xml

%changelog
* Fri Jul 08 2016 xiaotian.wu@i-soft.com.cn - 1.3.2-2
- rebuilt

* Tue Apr 19 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 1.3.2-1
- 1.3.2
