%global debug_package %{nil}

Name: clonezilla
Version: 3.10.11
Release: 1
License: GPL

Source0: http://free.nchc.org.tw/drbl-core/src/stable/clonezilla-3.10.11.tar.bz2
Patch0:usrbin.patch
BuildRequires: drbl partclone ntfsprogs partimage pigz fuse-sshfs parted-devel gdisk 

Summary:The Free and Open Source Software for Disk Imaging and Cloning
Requires: drbl partclone ntfsprogs partimage pigz fuse-sshfs parted gdisk

%description
The Free and Open Source Software for Disk Imaging and Cloning

%prep
%setup -q -T -c -n clonezilla -b0 
cd "%{_builddir}/%{name}/%{name}-%{version}"
%patch0  -p0 

%build 

%install
cd "%{_builddir}/%{name}"/%{name}-%{version}
make DESTDIR="%{buildroot}"/ install  

%files
%{_sysconfdir}/drbl/drbl-ocs.conf
%{_bindir}/clonezilla
%{_bindir}/cnvt-ocs-dev
%{_bindir}/create-cciss-mapping
%{_bindir}/create-debian-live
%{_bindir}/create-drbl-live
%{_bindir}/create-drbl-live-by-pkg
%{_bindir}/create-gparted-live
%{_bindir}/create-ocs-tmp-img
%{_bindir}/create-ubuntu-live
%{_bindir}/cv-ocsimg-v1-to-v2
%{_bindir}/drbl-ocs
%{_bindir}/drbl-ocs-live-prep
%{_bindir}/get-latest-ocs-live-ver
%{_bindir}/ocs-chkimg
%{_bindir}/ocs-chnthn
%{_bindir}/ocs-cnvt-usb-zip-to-dsk
%{_bindir}/ocs-cvtimg-comp
%{_bindir}/ocs-devsort
%{_bindir}/ocs-expand-mbr-pt
%{_bindir}/ocs-gen-grub2-efi-bldr
%{_bindir}/ocs-get-part-info
%{_bindir}/ocs-install-grub
%{_bindir}/ocs-iso
%{_bindir}/ocs-lang-kbd-conf
%{_bindir}/ocs-langkbdconf-bterm
%{_bindir}/ocs-live
%{_bindir}/ocs-live-boot-menu
%{_bindir}/ocs-live-bug-report
%{_bindir}/ocs-live-dev
%{_bindir}/ocs-live-final-action
%{_bindir}/ocs-live-general
%{_bindir}/ocs-live-netcfg
%{_bindir}/ocs-live-post-run
%{_bindir}/ocs-live-pre-run
%{_bindir}/ocs-live-restore
%{_bindir}/ocs-live-run-menu
%{_bindir}/ocs-live-save
%{_bindir}/ocs-lvm2-start
%{_bindir}/ocs-lvm2-stop
%{_bindir}/ocs-makeboot
%{_bindir}/ocs-onthefly
%{_bindir}/ocs-put-signed-grub2-efi-bldr
%{_bindir}/ocs-related-srv
%{_bindir}/ocs-resize-part
%{_bindir}/ocs-restore-mbr
%{_bindir}/ocs-restore-mdisks
%{_bindir}/ocs-rm-win-swap-hib
%{_bindir}/ocs-socket
%{_bindir}/ocs-sr
%{_bindir}/ocs-srv-live
%{_bindir}/ocs-tux-postprocess
%{_bindir}/ocs-update-initrd
%{_bindir}/ocs-update-syslinux
%{_bindir}/ocsmgrd
%{_bindir}/prep-ocsroot
%{_bindir}/update-efi-nvram-boot-entry
%{_datadir}/clonezilla/doc/AUTHORS
%{_datadir}/clonezilla/doc/ChangeLog.txt
%{_datadir}/clonezilla/doc/VERSION
%{_datadir}/drbl/postrun/ocs/00-readme.txt
%{_datadir}/drbl/prerun/ocs/00-readme.txt
%{_datadir}/drbl/samples/create-1P-pt-sf
%{_datadir}/drbl/samples/create-2P-pt-sf
%{_datadir}/drbl/samples/custom-ocs
%{_datadir}/drbl/samples/custom-ocs-1
%{_datadir}/drbl/samples/custom-ocs-2
%{_datadir}/drbl/samples/gen-netcfg
%{_datadir}/drbl/samples/gen-rec-usb
%{_datadir}/drbl/sbin/ocs-chnthn-functions
%{_datadir}/drbl/sbin/ocs-functions
%{_datadir}/drbl/sbin/set-netboot-1st-efi-nvram
%{_datadir}/drbl/setup/files/gparted/fluxbox/apps
%{_datadir}/drbl/setup/files/gparted/fluxbox/menu
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S02cmdline
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S03prep-gparted-live
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S05kbd-conf
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S07choose-lang
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S08pre-run
%{_datadir}/drbl/setup/files/gparted/gparted-live.d/S09start-X
%{_datadir}/drbl/setup/files/gparted/ideskrc
%{_datadir}/drbl/setup/files/gparted/idesktop/exit.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/gparted.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/lxrandr.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/netcfg.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/netsurf.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/screenshot.lnk
%{_datadir}/drbl/setup/files/gparted/idesktop/terminal.lnk
%{_datadir}/drbl/setup/files/gparted/image/Gsplash.png
%{_datadir}/drbl/setup/files/gparted/live-hook/efi-binary-hook
%{_datadir}/drbl/setup/files/gparted/live-hook/gparted-live-hook
%{_datadir}/drbl/setup/files/gparted/live-hook/start-gparted-live
%{_datadir}/drbl/setup/files/gparted/usr/bin/MC_HxEd
%{_datadir}/drbl/setup/files/gparted/usr/bin/gl-gen-grub2-efi-bldr
%{_datadir}/drbl/setup/files/gparted/usr/bin/gl-get-ipadd
%{_datadir}/drbl/setup/files/gparted/usr/bin/gl-killx
%{_datadir}/drbl/setup/files/gparted/usr/bin/gl-screenshot
%{_datadir}/drbl/setup/files/gparted/usr/sbin/Forcevideo
%{_datadir}/drbl/setup/files/gparted/usr/sbin/gl-live-netcfg
%{_datadir}/drbl/setup/files/gparted/usr/sbin/gl-shutdown-menu
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/bin/gl-functions
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/check-bash-lang
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/de_DE
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/de_DE.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/en_US
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/en_US.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/es_ES
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/es_ES.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/fr_FR
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/fr_FR.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/it_IT
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/it_IT.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/ja_JP.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/pt_BR
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/pt_BR.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/ru_RU.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/zh_CN.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/gparted/lang/zh_TW.UTF-8
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/00-README.txt
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/exit.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/gparted.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/info.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/lxrandr.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/netcfg.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/screenshot.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/shutdown-menu.xpm
%{_datadir}/drbl/setup/files/gparted%{_datadir}/pixmaps/terminal.xpm
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/K06post-run
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S00drbl-start
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S02cmdline
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S03prep-drbl-clonezilla
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S05kbd-conf
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S06pre-run
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S09config-X
%{_datadir}/drbl/setup/files/ocs/drbl-live.d/S99drbl-stop
%{_datadir}/drbl/setup/files/ocs/live-hook/drbl-live-hook
%{_datadir}/drbl/setup/files/ocs/live-hook/efi-binary-hook
%{_datadir}/drbl/setup/files/ocs/live-hook/ocs-live-hook
%{_datadir}/drbl/setup/files/ocs/live-hook/ocs-live-hook-functions
%{_datadir}/drbl/setup/files/ocs/live-hook/ocs-live-hook.conf
%{_datadir}/drbl/setup/files/ocs/live-hook/start-drbl-live
%{_datadir}/drbl/setup/files/ocs/live-hook/start-ocs-live
%{_datadir}/drbl/setup/files/ocs/live-hook/stop-drbl-live
%{_datadir}/drbl/setup/files/ocs/live-hook/stop-ocs-live
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/00_README.txt
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS0
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS0.conf
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS1
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS1.conf
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS2
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS2.conf
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS3
%{_datadir}/drbl/setup/files/ocs/live-hook/upstart/ttyS3.conf
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S00ocs-start
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S02cmdline
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S03prep-drbl-clonezilla
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S05-lang-kbd-conf
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S07arm-wol
%{_datadir}/drbl/setup/files/ocs/ocs-live.d/S99ocs-end
%{_datadir}/drbl/setup/files/ocs/ocs-run


%changelog
* Mon Dec 21 2015 kun.li@i-soft.com.cn - 3.10.11-1
- rebuilt

