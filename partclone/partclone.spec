Name: partclone
Version: 0.2.76
Release: 1
License: GPL

Source0: https://github.com/Thomas-Tsai/partclone/archive/0.2.76.tar.gz
BuildRequires: reiserfsprogs ntfs-3g libuuid-devel e2fsprogs-devel ncurses-devel

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
