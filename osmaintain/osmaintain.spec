Name: osmaintain
Version: 0.1.4
Release: 1
Summary: isoft system maintain tools
License: isoft
URL: http://git.isoft.zhcn.cc/wangguofeng/osmaintain
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: parted-devel
BuildRequires: qt5-qtbase-devel qt5-qttools-devel
BuildRequires: mesa-libGL-devel mesa-libgbm-devel libGLU-devel
Requires: parted qt5-qtbase
Requires: gparted
Requires: partclone
Requires: clonezilla

%description
isoft system maintain tools

%prep
%setup -n %{name}-%{version}

%build
cmake .
make

%install
make install DESTDIR=%{buildroot}

%files
/usr/sbin/osmaintain
/usr/sbin/sysbackup.sh
%{_datadir}/applications/osmaintain.desktop
%{_datadir}/apps/osmaintain/icons/isoft-logo.png
%{_datadir}/apps/osmaintain/trans/osmaintain_zh.qm

%changelog
* Fri Jan 08 2016 sulit <sulitsrc@gmail.com> - 0.1.4-1
- update version and fix partclone error

* Wed Jan 06 2016 sulit <sulitsrc@gmail.com> - 0.1-3
- many modification, and item 2,3 can be called successfully

* Tue Jan 05 2016 sulit <sulitsrc@gmail.com> - 0.1-2
- Init for isoft4
