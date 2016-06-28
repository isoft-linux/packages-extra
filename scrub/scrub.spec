Name:		scrub
Version:	2.5.2
Release:	1
Summary:	Disk scrubbing program
License:	GPLv2+
Group:		System Environment/Base
URL:		http://code.google.com/p/diskscrub/
Source0:	http://diskscrub.googlecode.com/files/%{name}-%{version}.tar.bz2

%description
Scrub writes patterns on files or disk devices to make
retrieving the data more difficult.  It operates in one of three
modes: 1) the special file corresponding to an entire disk is scrubbed
and all data on it is destroyed;  2) a regular file is scrubbed and
only the data in the file (and optionally its name in the directory
entry) is destroyed; or 3) a regular file is created, expanded until
the file system is full, then scrubbed as in 2).

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%doc DISCLAIMER COPYING
%doc README ChangeLog
%{_bindir}/scrub
%{_mandir}/man1/scrub.1*

%changelog
* Wed Apr 27 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.5.2-1
- add for libvirt

