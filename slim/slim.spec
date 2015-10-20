Name:           slim
Version:        1.3.6
Release:        1 
Summary:        Simple Login Manager
Group:          User Interface/X
License:        GPLv2+
URL:            http://slim.berlios.de/
Source0:        http://download.berlios.de/slim/%{name}-%{version}.tar.gz
Source1:        %{name}.pam

# adapted from debian to use freedesktop
Source2:        slim-update_slim_wmlist
Source3:        slim-dynwm

Source6:        slim-tmpfiles.conf
Source7:        slim.service

Patch1:         slim-customize.patch 

BuildRequires:  libXmu-devel libXft-devel libXrender-devel
BuildRequires:  libpng-devel libjpeg-devel freetype-devel fontconfig-devel
BuildRequires:  pkgconfig gettext pam-devel cmake
BuildRequires:  xterm freeglut-devel libXrandr-devel
Requires:       xterm /sbin/shutdown
Requires:       %{_sysconfdir}/pam.d
# we use 'include' in the pam file, so
Requires:       pam >= 0.80

BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
SLiM (Simple Login Manager) is a graphical login manager for X11.
It aims to be simple, fast and independent from the various
desktop environments.
SLiM is based on latest stable release of Login.app by Per Lidén.

In the distribution, slim may be called through a wrapper, slim-dynwm,
which determines the available window managers using the freedesktop
information and modifies the slim configuration file accordingly,
before launching slim.

%prep
%setup -q

%patch1 -p0 -b .fedora

%build
CXXFLAGS="%{optflags}" cmake -DUSE_PAM=yes -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

chmod 0644 %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m755 %{buildroot}%{_sysconfdir}/pam.d
install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
install -p -D %{SOURCE6} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/%{name}.service

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun

%files
%doc COPYING ChangeLog README* THEMES TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%ghost %dir %{_localstatedir}/run/%{name}
%{_bindir}/%{name}*
%{_mandir}/man1/%{name}*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes/
%{_unitdir}/%{name}.service
%{_libdir}/lib%{name}.so.%{version}

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf

