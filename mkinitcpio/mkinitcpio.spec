%define debug_package %{nil}

Name:		mkinitcpio
Version:	18
Release:	1
Summary:	mkinitcpio

Group:		core
License:	GPL
URL:		https://projects.archlinux.org/mkinitcpio.git/
Source0:	https://projects.archlinux.org/mkinitcpio.git/%{name}-%{version}.tar.gz

BuildRequires:	bash
Requires:	kernel

%description
mkinitcpio

%prep
%setup -n %{name}-%{version}


%build
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install


%files
/etc/mkinitcpio.conf
/usr/bin/lsinitcpio
/usr/bin/mkinitcpio
/usr/lib/initcpio/*
/usr/lib/kernel/install.d/50-mkinitcpio.install
/usr/lib/systemd/system/mkinitcpio-generate-shutdown-ramfs.service
/usr/lib/systemd/system/shutdown.target.wants/mkinitcpio-generate-shutdown-ramfs.service
/usr/lib/tmpfiles.d/mkinitcpio.conf
/usr/share/bash-completion/completions/lsinitcpio
/usr/share/bash-completion/completions/mkinitcpio
/usr/share/man/man1/lsinitcpio.1.gz
/usr/share/man/man5/mkinitcpio.conf.5.gz
/usr/share/man/man8/mkinitcpio.8.gz
/usr/share/mkinitcpio/example.preset
/usr/share/zsh/site-functions/_mkinitcpio


%changelog
* Sun Nov 29 2015 sulit <sulitsrc@gmail.com> - 18-1
- init for isoft4.0
