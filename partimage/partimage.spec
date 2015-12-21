Name: partimage
Version: 0.6.9
Release: 4
License: GPL

Source0: http://downloads.sourceforge.net/partimage/partimage-0.6.9.tar.bz2
Source1: partimaged-gencrt
Source2: partimaged.service
Patch0: partimage-0.6.9-zlib-1.2.6.patch
BuildRequires: newt-devel lzo-devel bzip2-devel openssl-devel 

Summary:Partition Image saves partitions in many formats to an image file.
Requires: newt lzo bzip2 openssl

%description
Partition Image saves partitions in many formats to an image file.

%prep
%autosetup -p1 -n %{name}-%{version}%{?prever}

%build 
%{configure}
make
make pamfile


%install
make DESTDIR="%{buildroot}" install
install -Dm0644 partimaged.pam "%{buildroot}/etc/pam.d/partimaged"
install -Dm0755 "%{SOURCE1}" "%{buildroot}/usr/bin/partimaged-gencrt"
chmod 644 "%{buildroot}/etc/partimaged/partimagedusers"
install -Dm0755 "%{SOURCE2}" "%{buildroot}/usr/lib/systemd/system/partimaged.service"
%find_lang %{name}

%files -f %{name}.lang
%{_sysconfdir}/pam.d/partimaged
%{_sysconfdir}/partimaged/partimagedusers
%{_bindir}/partimaged-gencrt
%{_libdir}/systemd/system/partimaged.service
%{_sbindir}/partimage
%{_sbindir}/partimaged
%{_docdir}/partimage/AUTHORS
%{_docdir}/partimage/BUGS
%{_docdir}/partimage/COPYING
%{_docdir}/partimage/ChangeLog
%{_docdir}/partimage/README
%{_docdir}/partimage/README.partimaged
%{_docdir}/partimage/partimage.lsm

%post
chown partimag:partimag /etc/partimaged/partimagedusers

%pre
groupadd -g 110 partimag &> /dev/null
useradd -u 110 -g partimag -c "Partimage user" -d /dev/null -s /bin/false partimag &> /dev/null

%postun
userdel partimag > /dev/null
groupdel partimag > /dev/null

%changelog
* Mon Dec 21 2015 kun.li@i-soft.com.cn - 0.6.9-4
- rebuilt

