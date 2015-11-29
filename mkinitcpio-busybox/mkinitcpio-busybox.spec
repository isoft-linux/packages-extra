Name: mkinitcpio-busybox
Version: 1.21.1
Release: 2
License: GPL

Source0: http://busybox.net/downloads/busybox-1.21.1.tar.bz2

Summary:base initramfs tools
Requires: glibc
Provides: /usr/bin/ash

%description
mkinitcpio-busybox

%prep
%setup -n  busybox-%{version}

%install
make
install -Dm755 busybox  %{buildroot}/usr/lib/initcpio/busybox

%files
/usr/lib/initcpio/busybox

%changelog
* Sun Nov 29 2015 sulit <sulitsrc@gmail.com> 1.21.1-2
- init for isoft4
