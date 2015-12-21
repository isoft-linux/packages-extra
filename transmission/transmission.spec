%global _hardened_build 1

Name:           transmission
Version:        2.84
Release:        11%{?dist}
Summary:        A lightweight GTK+ BitTorrent client

# See COPYING. This licensing situation is... special.
License:        MIT and GPLv2
URL:            http://www.transmissionbt.com
Source0:        http://download.transmissionbt.com/files/transmission-%{version}.tar.xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1221292
Source1:        https://raw.githubusercontent.com/gnome-design-team/gnome-icons/master/apps-symbolic/Adwaita/scalable/apps/transmission-symbolic.svg

BuildRequires:  openssl-devel >= 0.9.4
BuildRequires:  glib2-devel >= 2.32.0
BuildRequires:  gtk3-devel >= 3.2.0
BuildRequires:  libnotify-devel >= 0.4.3
BuildRequires:  libcanberra-devel
BuildRequires:  libcurl-devel >= 7.16.3
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  libevent-devel >= 2.0.10
BuildRequires:  desktop-file-utils
BuildRequires:  gettext intltool
BuildRequires:  qt5-qtbase-devel
BuildRequires:  systemd-devel
Requires: transmission-cli
Requires: transmission-gtk


%description
Transmission is a free, lightweight BitTorrent client. It features a
simple, intuitive interface on top on an efficient, cross-platform
back-end.

%package common
Summary:       Transmission common files
Conflicts:     transmission < 1.80-0.3.b4
%description common
Common files for Transmission BitTorrent client sub-packages. It includes 
the web user interface, icons and transmission-remote, transmission-create, 
transmission-edit, transmission-show utilities.

%package cli
Summary:       Transmission command line implementation
Requires:      transmission-common
Provides:      transmission = %{version}-%{release}
%description cli
Command line version of Transmission BitTorrent client.

%package daemon
Summary:       Transmission daemon
Requires:      transmission-common
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Provides:      transmission = %{version}-%{release}
%description daemon
Transmission BitTorrent client daemon.

%package gtk
Summary:       Transmission GTK interface
Requires:      transmission-common
Provides:      transmission = %{version}-%{release}

%description gtk
GTK graphical interface of Transmission BitTorrent client.

%package qt
Summary:       Transmission Qt interface
Requires:      transmission-common

%description qt
Qt graphical interface of Transmission BitTorrent client.

%pre daemon
getent group transmission >/dev/null || groupadd -r transmission
getent passwd transmission >/dev/null || \
useradd -r -g transmission -d %{_sharedstatedir}/transmission -s /sbin/nologin \
        -c "transmission daemon account" transmission
exit 0

%prep
%setup -q

# fix icon location for Transmission Qt
sed -i 's|Icon=%{name}-qt|Icon=%{name}|g' qt/%{name}-qt.desktop

# convert to UTF encoding
iconv --from=ISO-8859-1 --to=UTF-8 AUTHORS > AUTHORS.new
mv AUTHORS.new AUTHORS
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build

CXXFLAGS="%{optflags} -fPIC"

%configure --disable-static --enable-utp --enable-daemon \
           --enable-nls --enable-cli --enable-daemon --with-systemd-daemon 
make %{?_smp_mflags}

pushd qt
	%{qmake_qt5}  qtr.pro
	make %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{_unitdir}
install -m0644 daemon/transmission-daemon.service  %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sharedstatedir}/transmission
%make_install
make install INSTALL_ROOT=%{buildroot}%{_prefix} -C qt

# Install the symbolic icon
mkdir -p  %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/transmission-symbolic.svg

%find_lang %{name}-gtk

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gtk.desktop
desktop-file-install \
                --dir=%{buildroot}%{_datadir}/applications/  \
                  qt/%{name}-qt.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/transmission-gtk.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://forum.transmissionbt.com/viewtopic.php?f=3&t=16443
SentUpstream: 2014-09-18
-->
<application>
  <id type="desktop">transmission-gtk.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      BitTorrent is a peer-to-peer file-sharing protocol that is commonly used to
      distribute large amounts of data between multiple users.
    </p>
    <p>
      Transmission is a BitTorrent client with an easy-to-use frontend on top a
      cross-platform backend.
      Native frontends are available for OS X and Windows, as well as command line and
      web frontends.
    </p>
    <p>
      Notable features of Transmission include Local Peer Discovery and Full Encryption,
      Full encryption, DHTµTP, PEX and Magnet Link support.
    </p>
  </description>
  <url type="homepage">http://www.transmissionbt.com/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/transmission-gtk/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

%post common
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post gtk
/usr/bin/update-desktop-database &> /dev/null || :

%post qt
/usr/bin/update-desktop-database &> /dev/null || :

%post daemon
%systemd_post transmission-daemon.service

%preun daemon
%systemd_preun transmission-daemon.service

%postun common
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun daemon
%systemd_postun_with_restart transmission-daemon.service

%postun gtk
/usr/bin/update-desktop-database &> /dev/null || :

%postun qt
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans common
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files

%files common
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/transmission-remote
%{_bindir}/transmission-create
%{_bindir}/transmission-edit
%{_bindir}/transmission-show
%{_datadir}/transmission/
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/transmission.*
%{_datadir}/icons/hicolor/symbolic/apps/transmission-symbolic.svg
%doc %{_mandir}/man1/transmission-remote*
%doc %{_mandir}/man1/transmission-create*
%doc %{_mandir}/man1/transmission-edit*
%doc %{_mandir}/man1/transmission-show*

%files cli
%{_bindir}/transmission-cli
%doc %{_mandir}/man1/transmission-cli*

%files daemon
%{_bindir}/transmission-daemon
%{_unitdir}/transmission-daemon.service
%attr(-,transmission, transmission)%{_sharedstatedir}/transmission/
%doc %{_mandir}/man1/transmission-daemon*

%files gtk -f %{name}-gtk.lang
%{_bindir}/transmission-gtk
%{_datadir}/appdata/%{name}-gtk.appdata.xml
%{_datadir}/applications/transmission-gtk.desktop
%doc %{_mandir}/man1/transmission-gtk.*

%files qt
%{_bindir}/transmission-qt
%{_datadir}/applications/transmission-qt.desktop
%doc %{_mandir}/man1/transmission-qt.*

%changelog
* Mon Dec 21 2015 sulit <sulitsrc@gmail.com> - 2.84-11
- Remove Group info

* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 2.84-10
- update release

* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 2.84-9
- Init for isoft4
- qt:	1. functions support ok
-	2. support session
-	3. no chinese UI support
-	4. no logs item in menu help
- gtk:	1. functions support seem worse(I think)
- 	2. has logs item in menu help
- 	3. chinese UI support ok
- sum: which one will be selected?
