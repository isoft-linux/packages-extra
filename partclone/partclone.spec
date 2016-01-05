Name: partclone
Version: 0.2.76
Release: 2
License: GPL

Source0: https://github.com/Thomas-Tsai/partclone/archive/0.2.76.tar.gz
BuildRequires: reiserfsprogs ntfs-3g-devel libuuid-devel e2fsprogs-devel ncurses-devel libblkid-devel

Summary:Utilities to save and restore used blocks on a partition
Requires: reiserfsprogs ntfs-3g e2fsprogs ncurses

%description
Utilities to save and restore used blocks on a partition

%prep
%setup -q -T -c -n partclone -b0 

%build 
cd "%{_builddir}"/%{name}/%{name}-%{version}
%{configure} --enable-extfs --enable-fat  --enable-exfat --enable-ntfs --enable-btrfs  --enable-ncursesw --enable-mtrace 

make  %{?_smp_mflags}

%install
cd "%{_builddir}"/%{name}/%{name}-%{version}
make PREFIX=/usr DESTDIR="%{buildroot}" install

%files 
%{_mandir}/man8/partclone.btrfs.8.gz
%{_mandir}/man8/partclone.ext2.8.gz
%{_mandir}/man8/partclone.ext3.8.gz
%{_mandir}/man8/partclone.ext4.8.gz
%{_mandir}/man8/partclone.ext4dev.8.gz
%{_mandir}/man8/partclone.extfs.8.gz
%{_mandir}/man8/partclone.fat.8.gz
%{_mandir}/man8/partclone.fat12.8.gz
%{_mandir}/man8/partclone.fat16.8.gz
%{_mandir}/man8/partclone.fat32.8.gz
%{_mandir}/man8/partclone.ntfs.8.gz
%{_mandir}/man8/partclone.ntfsfixboot.8.gz
%{_mandir}/man8/partclone.vfat.8.gz
%{_sbindir}/partclone.btrfs
%{_sbindir}/partclone.exfat
%{_sbindir}/partclone.ext2
%{_sbindir}/partclone.ext3
%{_sbindir}/partclone.ext4
%{_sbindir}/partclone.ext4dev
%{_sbindir}/partclone.extfs
%{_sbindir}/partclone.fat
%{_sbindir}/partclone.fat12
%{_sbindir}/partclone.fat16
%{_sbindir}/partclone.fat32
%{_sbindir}/partclone.ntfs
%{_sbindir}/partclone.ntfsreloc
%{_sbindir}/partclone.vfat
%{_mandir}/man8/partclone.exfat.8.gz
%{_mandir}/man8/partclone.ntfsreloc.8.gz
%{_sbindir}/partclone.chkimg
%{_sbindir}/partclone.dd
%{_sbindir}/partclone.imager
%{_sbindir}/partclone.info
%{_sbindir}/partclone.ntfsfixboot
%{_sbindir}/partclone.restore
%{_datadir}/locale/fr_FR/LC_MESSAGES/partclone.mo
%{_datadir}/locale/vi/LC_MESSAGES/partclone.mo
%{_datadir}/locale/zh_TW/LC_MESSAGES/partclone.mo
%{_datadir}/partclone/fail-mbr.bin
%{_mandir}/man8/partclone.8.gz
%{_mandir}/man8/partclone.chkimg.8.gz
%{_mandir}/man8/partclone.dd.8.gz
%{_mandir}/man8/partclone.imager.8.gz
%{_mandir}/man8/partclone.info.8.gz
%{_mandir}/man8/partclone.restore.8.gz

%changelog
* Mon Dec 21 2015 kun.li@i-soft.com.cn - 3.10.11-1
- rebuilt
