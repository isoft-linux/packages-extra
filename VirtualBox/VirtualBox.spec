#
# Spec file for creating VirtualBox rpm packages
#

#
# Copyright (C) 2006-2015 Oracle Corporation
#
# This file is part of VirtualBox Open Source Edition (OSE), as
# available from http://www.virtualbox.org. This file is free software;
# you can redistribute it and/or modify it under the terms of the GNU
# General Public License (GPL) as published by the Free Software
# Foundation, in version 2 as it comes in the "COPYING" file of the
# VirtualBox OSE distribution. VirtualBox OSE is distributed in the
# hope that it will be useful, but WITHOUT ANY WARRANTY of any kind.
#

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:   Oracle VM VirtualBox
Name:      VirtualBox
Version:   5.1.2
Release:   1
URL:       http://www.virtualbox.org/
Source:    http://download.virtualbox.org/virtualbox/5.0.10/%{name}-%{version}.tar.bz2
License:   GPLv2

# BuildRequires:  SDL-devel xalan-c-devel
BuildRequires:  SDL-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
# BuildRequires:  iasl libxslt-devel xerces-c-devel libIDL-devel
BuildRequires:  acpica-tools libxslt-devel libIDL-devel
BuildRequires:  yasm
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
BuildRequires:  qt4-devel
# BuildRequires:  gsoap-devel
BuildRequires:  pam-devel
BuildRequires:  cdrkit
BuildRequires:  boost-devel
# BuildRequires:  liblzf-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  device-mapper-devel
BuildRequires:  libvpx-devel
BuildRequires:  makeself

BuildRequires:  /usr/lib/libc.so
BuildRequires:  /usr/lib/libstdc++.so.6 /lib/libc.so.6

# For the X11 module
BuildRequires:  libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  pixman-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-server-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXmu-devel
BuildRequires:  sed

BuildRequires: systemd-units
Requires: dkms-%{name}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: kernel-headers

# Plague-specific weirdness
ExclusiveArch:  x86_64


%description
VirtualBox is a powerful PC virtualization solution allowing
you to run a wide range of PC operating systems on your Linux
system. This includes Windows, Linux, FreeBSD, DOS, OpenBSD
and others. VirtualBox comes with a broad feature set and
excellent performance, making it the premier virtualization
software solution on the market.

%package -n dkms-%{name}
Summary: VirtualBox dkms pkg

%description -n dkms-%{name}
VirtualBox dkms pkg.


%prep
%setup -q -D


%build
sed -e 's/PACKAGE_NAME="vboxhost"/PACKAGE_NAME="%{name}"/' -i src/VBox/HostDrivers/linux/dkms.conf
sed -e 's/PACKAGE_VERSION=.*/PACKAGE_VERSION="%{version}"/' -i src/VBox/HostDrivers/linux/dkms.conf
sed -e "s/WITH_VMMRAW=1/WITH_VMMRAW=0/" -i configure
sed -e "s/WITH_KMODS=1/WITH_KMODS=0/" -i configure

./configure --disable-hardening --disable-java --disable-docs

source ./env.sh
kmk


%install
OUTPRE=out/linux.amd64/release/bin
# cd %{name}-%{version}/$OUTPRE
cd $OUTPRE
# Mandriva: prevent replacing 'echo' by 'gprintf'
export DONT_GPRINTIFY=1
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT/sbin
install -m 755 -d $RPM_BUILD_ROOT%{_initrddir}
install -m 755 -d $RPM_BUILD_ROOT/lib/modules
install -m 755 -d $RPM_BUILD_ROOT/etc/vbox
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 755 -d $RPM_BUILD_ROOT/usr/src
install -m 755 -d $RPM_BUILD_ROOT/usr/share/applications
install -m 755 -d $RPM_BUILD_ROOT/usr/share/pixmaps
install -m 755 -d $RPM_BUILD_ROOT/usr/share/icons/hicolor
install -m 755 -d $RPM_BUILD_ROOT%{_defaultdocdir}/virtualbox
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/virtualbox
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/virtualbox/ExtensionPacks
install -m 755 -d $RPM_BUILD_ROOT/usr/share/virtualbox
install -m 755 -d $RPM_BUILD_ROOT/usr/share/mime/packages
install -m 755 -d $RPM_BUILD_ROOT/usr/src/%{name}-%{version}/
mv VBoxEFI32.fd $RPM_BUILD_ROOT/usr/lib/virtualbox || true
mv VBoxEFI64.fd $RPM_BUILD_ROOT/usr/lib/virtualbox || true
mv *.rc $RPM_BUILD_ROOT/usr/lib/virtualbox || true
mv *.r0 $RPM_BUILD_ROOT/usr/lib/virtualbox
mv *.rel $RPM_BUILD_ROOT/usr/lib/virtualbox || true
mv VBoxNetDHCP $RPM_BUILD_ROOT/usr/lib/virtualbox
mv VBoxNetNAT $RPM_BUILD_ROOT/usr/lib/virtualbox
mv VBoxNetAdpCtl $RPM_BUILD_ROOT/usr/lib/virtualbox
if [ -f VBoxVolInfo ]; then
  mv VBoxVolInfo $RPM_BUILD_ROOT/usr/lib/virtualbox
fi
mv ../obj/VBoxXPCOMIPCD/VBoxXPCOMIPCD $RPM_BUILD_ROOT/usr/lib/virtualbox
mv components $RPM_BUILD_ROOT/usr/lib/virtualbox/components
mv *.so $RPM_BUILD_ROOT/usr/lib/virtualbox
mv *.so.4 $RPM_BUILD_ROOT/usr/lib/virtualbox || true
ln -s ../VBoxVMM.so $RPM_BUILD_ROOT/usr/lib/virtualbox/components/VBoxVMM.so
mv VBoxTestOGL $RPM_BUILD_ROOT/usr/lib/virtualbox
mv vboxshell.py $RPM_BUILD_ROOT/usr/lib/virtualbox
(export VBOX_INSTALL_PATH=/usr/lib/virtualbox && \
  cd ./sdk/installer && \
  %{__python} ./vboxapisetup.py install --prefix %{_prefix} --root $RPM_BUILD_ROOT)
rm -rf sdk/installer
mv sdk $RPM_BUILD_ROOT/usr/lib/virtualbox
mv nls $RPM_BUILD_ROOT/usr/share/virtualbox
cp src/* $RPM_BUILD_ROOT/usr/src/%{name}-%{version} -R
mv src $RPM_BUILD_ROOT/usr/share/virtualbox
mv VBox.sh $RPM_BUILD_ROOT/usr/bin/VBox
mv VBoxSysInfo.sh $RPM_BUILD_ROOT/usr/share/virtualbox
mv VBoxCreateUSBNode.sh $RPM_BUILD_ROOT/usr/share/virtualbox
cp icons/128x128/virtualbox.png $RPM_BUILD_ROOT/usr/share/pixmaps/virtualbox.png
cd icons
  for i in *; do
    if [ -f $i/virtualbox.* ]; then
      install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/$i/apps
      mv $i/virtualbox.* $RPM_BUILD_ROOT/usr/share/icons/hicolor/$i/apps
    fi
    install -d $RPM_BUILD_ROOT/usr/share/icons/hicolor/$i/mimetypes
    mv $i/* $RPM_BUILD_ROOT/usr/share/icons/hicolor/$i/mimetypes || true
    rmdir $i
  done
cd -
rmdir icons
mv virtualbox.xml $RPM_BUILD_ROOT/usr/share/mime/packages
for i in VBoxManage VBoxSVC VirtualBox VBoxHeadless VBoxDTrace VBoxExtPackHelperApp VBoxBalloonCtrl VBoxAutostart vbox-img; do
  mv $i $RPM_BUILD_ROOT/usr/lib/virtualbox; done
if %WEBSVC%; then
  for i in vboxwebsrv webtest; do
    mv $i $RPM_BUILD_ROOT/usr/lib/virtualbox; done
fi
test -f VBoxSDL && mv VBoxSDL $RPM_BUILD_ROOT/usr/lib/virtualbox
for i in VirtualBox VBoxHeadless VBoxNetDHCP VBoxNetNAT VBoxNetAdpCtl; do
  chmod 4511 $RPM_BUILD_ROOT/usr/lib/virtualbox/$i; done
if [ -f $RPM_BUILD_ROOT/usr/lib/virtualbox/VBoxVolInfo ]; then
  chmod 4511 $RPM_BUILD_ROOT/usr/lib/virtualbox/VBoxVolInfo
fi
test -f VBoxSDL && chmod 4511 $RPM_BUILD_ROOT/usr/lib/virtualbox/VBoxSDL
if [ -d ExtensionPacks/VNC ]; then
  mv ExtensionPacks/VNC $RPM_BUILD_ROOT/usr/lib/virtualbox/ExtensionPacks
fi
mv VBoxTunctl $RPM_BUILD_ROOT/usr/bin
cat >> $RPM_BUILD_ROOT/sbin/vboxconfig << EOF
#!/bin/sh

name=%{name}
version=%{version}

echo "Please wait some seconds, building kernel modules..."
dkms add -m \$name -v \$version &> /dev/null
dkms build -m \$name -v \$version &> /dev/null
dkms install -m \$name -v \$version --force &> /dev/null
/sbin/depmod -a
/sbin/modprobe -a vboxdrv vboxnetadp vboxnetflt vboxpci
echo "OK! Restart \$name, and use it!"
EOF

chmod 755 $RPM_BUILD_ROOT/sbin/vboxconfig

# %if %{?is_ose:0}%{!?is_ose:1}
%if 0
for d in /lib/modules/*; do
  if [ -L $d/build ]; then
    rm -f /tmp/vboxdrv-Module.symvers
    ./src/vboxhost/build_in_tmp \
      --save-module-symvers /tmp/vboxdrv-Module.symvers \
      --module-source `pwd`/src/vboxhost/vboxdrv \
      KBUILD_VERBOSE= KERN_DIR=$d/build MODULE_DIR=$RPM_BUILD_ROOT/$d/misc -j4 \
      %INSTMOD%
    ./src/vboxhost/build_in_tmp \
      --use-module-symvers /tmp/vboxdrv-Module.symvers \
      --module-source `pwd`/src/vboxhost/vboxnetflt \
      KBUILD_VERBOSE= KERN_DIR=$d/build MODULE_DIR=$RPM_BUILD_ROOT/$d/misc -j4 \
      %INSTMOD%
    ./src/vboxhost/build_in_tmp \
      --use-module-symvers /tmp/vboxdrv-Module.symvers \
      --module-source `pwd`/src/vboxhost/vboxnetadp \
      KBUILD_VERBOSE= KERN_DIR=$d/build MODULE_DIR=$RPM_BUILD_ROOT/$d/misc -j4 \
      %INSTMOD%
    ./src/vboxhost/build_in_tmp \
      --use-module-symvers /tmp/vboxdrv-Module.symvers \
      --module-source `pwd`/src/vboxhost/vboxpci \
      KBUILD_VERBOSE= KERN_DIR=$d/build MODULE_DIR=$RPM_BUILD_ROOT/$d/misc -j4 \
      %INSTMOD%
  fi
done
%endif
%if 0
  mv kchmviewer $RPM_BUILD_ROOT/usr/lib/virtualbox
  for i in rdesktop-vrdp.tar.gz rdesktop-vrdp-keymaps; do
    mv $i $RPM_BUILD_ROOT/usr/share/virtualbox; done
  mv rdesktop-vrdp $RPM_BUILD_ROOT/usr/bin
%endif
for i in additions/VBoxGuestAdditions.iso; do
  mv $i $RPM_BUILD_ROOT/usr/share/virtualbox || true;
done
if [ -d accessible ]; then
  mv accessible $RPM_BUILD_ROOT/usr/lib/virtualbox
fi
cp src/vboxdrv.sh $RPM_BUILD_ROOT/usr/lib/virtualbox || true
mv vboxballoonctrl-service.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv vboxautostart-service.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv vboxweb-service.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv postinst-common.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv prerm-common.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv routines.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv loadall.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
mv load.sh $RPM_BUILD_ROOT/usr/lib/virtualbox
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VirtualBox
ln -s VBox $RPM_BUILD_ROOT/usr/bin/virtualbox
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxManage
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxmanage
test -f VBoxSDL && ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxSDL
test -f VBoxSDL && ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxsdl
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxVRDP
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxHeadless
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxheadless
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxDTrace
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxdtrace
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxBalloonCtrl
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxballoonctrl
ln -s VBox $RPM_BUILD_ROOT/usr/bin/VBoxAutostart
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxautostart
ln -s VBox $RPM_BUILD_ROOT/usr/bin/vboxwebsrv
ln -s /usr/lib/virtualbox/vbox-img $RPM_BUILD_ROOT/usr/bin/vbox-img
#ln -s /usr/share/virtualbox/src/ $RPM_BUILD_ROOT/usr/src/vboxhost-%{version}
mv virtualbox.desktop $RPM_BUILD_ROOT/usr/share/applications/virtualbox.desktop
mv VBox.png $RPM_BUILD_ROOT/usr/share/pixmaps/VBox.png


%pre
# defaults
[ -r /etc/default/virtualbox ] && . /etc/default/virtualbox

# check for old installation
if [ -r /etc/vbox/vbox.cfg ]; then
  . /etc/vbox/vbox.cfg
  if [ "x$INSTALL_DIR" != "x" -a -d "$INSTALL_DIR" ]; then
    echo "An old installation of VirtualBox was found. To install this package the"
    echo "old package has to be removed first. Have a look at /etc/vbox/vbox.cfg to"
    echo "determine the installation directory of the previous installation. After"
    echo "uninstalling the old package remove the file /etc/vbox/vbox.cfg."
    exit 1
  fi
fi

# check for active VMs of the installed (old) package
# Execute the installed packages pre-uninstaller if present.
/usr/lib/virtualbox/prerm-common.sh 2>/dev/null
# Stop services from older versions without pre-uninstaller.
/etc/init.d/vboxballoonctrl-service stop 2>/dev/null
/etc/init.d/vboxautostart-service stop 2>/dev/null
/etc/init.d/vboxweb-service stop 2>/dev/null
VBOXSVC_PID=`pidof VBoxSVC 2>/dev/null || true`
if [ -n "$VBOXSVC_PID" ]; then
  # ask the daemon to terminate immediately
  kill -USR1 $VBOXSVC_PID
  sleep 1
  if pidof VBoxSVC > /dev/null 2>&1; then
    echo "A copy of VirtualBox is currently running.  Please close it and try again."
    echo "Please note that it can take up to ten seconds for VirtualBox (in particular"
    echo "the VBoxSVC daemon) to finish running."
    exit 1
  fi
fi

# XXX remove old modules from previous versions (disable with INSTALL_NO_VBOXDRV=1 in /etc/default/virtualbox)
if [ "$INSTALL_NO_VBOXDRV" != "1" ]; then
  find /lib/modules -name "vboxdrv\.*" 2>/dev/null|xargs rm -f 2> /dev/null || true
  find /lib/modules -name "vboxnetflt\.*" 2>/dev/null|xargs rm -f 2> /dev/null || true
  find /lib/modules -name "vboxnetadp\.*" 2>/dev/null|xargs rm -f 2> /dev/null || true
  find /lib/modules -name "vboxpci\.*" 2>/dev/null|xargs rm -f 2> /dev/null || true
fi


%post
#include installer-common.sh

LOG="/var/log/vbox-install.log"

# defaults
[ -r /etc/default/virtualbox ] && . /etc/default/virtualbox

# remove old cruft
if [ -f /etc/init.d/vboxdrv.sh ]; then
  echo "Found old version of /etc/init.d/vboxdrv.sh, removing."
  rm /etc/init.d/vboxdrv.sh
fi
if [ -f /etc/vbox/vbox.cfg ]; then
  echo "Found old version of /etc/vbox/vbox.cfg, removing."
  rm /etc/vbox/vbox.cfg
fi
rm -f /etc/vbox/module_not_compiled


# create users groups (disable with INSTALL_NO_GROUP=1 in /etc/default/virtualbox)
if [ "$INSTALL_NO_GROUP" != "1" ]; then
  echo
  echo "Creating group 'vboxusers'. VM users must be member of that group!"
  echo
  groupadd -r -f vboxusers 2> /dev/null
fi

# install udev rule (disable with INSTALL_NO_UDEV=1 in /etc/default/virtualbox)
# and /dev/vboxdrv and /dev/vboxusb/*/* device nodes
install_device_node_setup root 0600 /usr/share/virtualbox "${usb_group}" &> /dev/null || true
%if %{?rpm_mdv:1}%{!?rpm_mdv:0}
/sbin/ldconfig
%update_menus || true
%endif
update-mime-database /usr/share/mime &> /dev/null || :
update-desktop-database -q > /dev/null 2>&1 || :
touch --no-create /usr/share/icons/hicolor
gtk-update-icon-cache -q /usr/share/icons/hicolor 2> /dev/null || :

%if 0
# Disable module compilation with INSTALL_NO_VBOXDRV=1 in /etc/default/virtualbox
BUILD_MODULES=0
REGISTER_MODULES=1
if [ ! -f /lib/modules/`uname -r`/misc/vboxdrv.ko ]; then
  REGISTER_MODULES=0
  if [ "$INSTALL_NO_VBOXDRV" != "1" ]; then
    # compile problem
    cat << EOF
No precompiled module for this kernel found -- trying to build one. Messages
emitted during module compilation will be logged to $LOG.

EOF
    BUILD_MODULES=1
  fi
fi
# if INSTALL_NO_VBOXDRV is set to 1, remove all shipped modules
if [ "$INSTALL_NO_VBOXDRV" = "1" ]; then
  rm -f /lib/modules/*/misc/vboxdrv.ko
  rm -f /lib/modules/*/misc/vboxnetflt.ko
  rm -f /lib/modules/*/misc/vboxnetadp.ko
  rm -f /lib/modules/*/misc/vboxpci.ko
fi
if [ $BUILD_MODULES -eq 1 ]; then
  /usr/lib/virtualbox/vboxdrv.sh setup || true
else
  if lsmod | grep -q "vboxdrv[^_-]"; then
    /usr/lib/virtualbox/vboxdrv.sh stop || true
  fi
fi
# Install and start the new service scripts.
PRERM_DKMS=
test "${REGISTER_MODULES}" = 1 && PRERM_DKMS="--dkms %{version}"
POSTINST_START=
test "${INSTALL_NO_VBOXDRV}" = 1 && POSTINST_START=--nostart
/usr/lib/virtualbox/prerm-common.sh ${PRERM_DKMS} || true
/usr/lib/virtualbox/postinst-common.sh ${POSTINST_START} > /dev/null || true
%endif

%posttrans -n dkms-%{name}
echo "Waiting ..."
(
dkms add -m %{name} -v %{version}
dkms build -m %{name} -v %{version}
dkms install -m %{name} -v %{version} --force
/sbin/depmod -a
/sbin/modprobe -a vboxdrv vboxnetadp vboxnetflt vboxpci
cat > /etc/modules-load.d/VirtualBox.conf << EOF
vboxdrv
vboxnetadp
vboxnetflt
vboxpci
EOF
) || :


%preun
# Called before the package is removed, or during upgrade after (not before)
# the new version's "post" scriptlet. 
# $1==0: remove the last version of the package
# $1>=1: upgrade
if [ "$1" = 0 ]; then
  /usr/lib/virtualbox/prerm-common.sh --dkms %{version} || exit 1
  rm -f /etc/udev/rules.d/60-vboxdrv.rules
  rm -f /etc/vbox/license_agreed
  rm -f /etc/vbox/module_not_compiled
fi

%preun -n dkms-%{name}
(
dkms uninstall -m %{name} -v %{version}
dkms remove -m %{name} -v %{version} --all
rm /etc/modules-load.d/VirtualBox.conf
/sbin/depmod -a
) || :


%postun
%if %{?rpm_mdv:1}%{!?rpm_mdv:0}
/sbin/ldconfig
%{clean_desktop_database}
%clean_menus
%endif
update-mime-database /usr/share/mime &> /dev/null || :
update-desktop-database -q > /dev/null 2>&1 || :
touch --no-create /usr/share/icons/hicolor
gtk-update-icon-cache -q /usr/share/icons/hicolor 2> /dev/null || :
rm -rf /usr/lib/virtualbox/ExtensionPacks


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%if 0
%doc %{!?is_ose: LICENSE}
%doc UserManual*.pdf
%doc %{!?is_ose: VirtualBox*.chm}
%{?rpm_suse: %{py_sitedir}/*}
%{!?rpm_suse: %{python_sitelib}/*}
%endif
/etc/vbox
/sbin/vboxconfig
/usr/bin/*
#/usr/src/vbox*
/usr/lib/virtualbox
/usr/share/applications/*
/usr/share/icons/hicolor/*/apps/*
/usr/share/icons/hicolor/*/mimetypes/*
/usr/share/mime/packages/*
/usr/share/pixmaps/*
/usr/share/virtualbox
%{python_sitelib}/*

%files -n dkms-%{name}
/usr/src/%{name}-%{version}

%changelog
* Mon Aug 08 2016 sulit <sulitsrc@gmail.com> - 5.1.2-1
- upgrade to official version

* Mon Apr 18 2016 sulit <sulitsrc@gmail.com> - 5.0.16-2
- update virtualbox to 5.0.16 and modify dkms.conf

* Thu Jan 07 2016 sulit <sulitsrc@gmail.com> - 5.0.12-1
- add vboxconfig prompt
- remove check_gcc_version patch
- upgrade 5.0.12

* Thu Dec 24 2015 sulit <sulitsrc@gmail.com> - 5.0.10-5
- packge /sbin/vboxconfig file

* Thu Dec 24 2015 sulit <sulitsrc@gmail.com> - 5.0.10-4
- add /sbin/vboxconfig file
- add requires kernel-headers

* Mon Dec 14 2015 sulit <sulitsrc@gmail.com> - 5.0.10-3
- redirect output to /dev/null and add wait note
- enable kernel default load vbox*.ko

* Mon Dec 14 2015 sulit <sulitsrc@gmail.com> - 5.0.10-2
- Init for isoft4
- add cdrkit buildrequire
- disable kmods

