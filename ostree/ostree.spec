Summary: Tool for managing bootable, immutable filesystem trees
Name: ostree
Version: 2016.15
Release: 2
#VCS: git:git://git.gnome.org/ostree
Source0: http://ftp.gnome.org/pub/GNOME/sources/ostree/%{version}/ostree-%{version}.tar.xz
Source1: 91-ostree.preset
License: LGPLv2+
URL: http://live.gnome.org/OSTree

BuildRequires: git
# We always run autogen.sh
BuildRequires: autoconf automake libtool
# For docs
BuildRequires: gtk-doc
# Core requirements
BuildRequires: pkgconfig(libgsystem) >= 2015.1
BuildRequires: pkgconfig(libsoup-2.4)
BuildRequires: libattr-devel
# Extras
BuildRequires: pkgconfig(libarchive)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libselinux)
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(e2p)
BuildRequires: libcap-devel
BuildRequires: gpgme-devel
BuildRequires: pkgconfig(systemd)
BuildRequires: /usr/bin/g-ir-scanner
BuildRequires: dracut
BuildRequires:  bison

# Runtime requirements
Requires: libgsystem >= 2015.1
Requires: dracut
Requires: /usr/bin/gpgv2
Requires: systemd-units

Patch2: 0001-ostree-remount-Explicitly-set-tmp-to-01777.patch

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package devel
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: %{name} =  %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%ifnarch s390 s390x %{arm}
%package grub2
Summary: GRUB2 integration for OSTree
Group: Development/Libraries
%ifnarch aarch64
Requires: grub2
%else
Requires: grub2-efi
%endif

%description grub2
GRUB2 integration for OSTree
%endif

%prep
%autosetup -Sgit -n ostree-%{version}

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules \
	   --enable-gtk-doc \
	   --with-selinux \
	   --with-dracut
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
find $RPM_BUILD_ROOT -name '*.la' -delete
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system-preset/91-ostree.preset


%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
#%{_sbindir}/ostree-prepare-root
#%{_sbindir}/ostree-remount
%{_datadir}/ostree/trusted.gpg.d
%{_sysconfdir}/ostree
%{_sysconfdir}/dracut.conf.d/ostree.conf
%dir %{_prefix}/lib/dracut/modules.d/98ostree
#%{_prefix}/lib/systemd/system/ostree*.service
%{_prefix}/lib/dracut/modules.d/98ostree/*
%{_libdir}/ostree/ostree-prepare-root
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib
%{_mandir}/man*/*.gz
%{_prefix}/lib/systemd/system-preset/91-ostree.preset
%exclude %{_sysconfdir}/grub.d/*ostree
%exclude %{_libexecdir}/ostree/grub2*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%dir %{_datadir}/gtk-doc/html/ostree
%{_datadir}/gtk-doc/html/ostree
%{_datadir}/gir-1.0/OSTree-1.0.gir

%ifnarch s390 s390x %{arm}
%files grub2
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/ostree/grub2*
%endif

%changelog
* Mon Dec 26 2016 sulit - 2016.15-2
- rebuild ostree

* Mon Dec 26 2016 sulit - 2016.15-1
- upgrade ostree to 2016.15

* Tue Jun 28 2016 fj <fujiang.zhu@i-soft.com.cn> - 2016.6-2
- rebuilt for flatpak
