Name: virt-viewer
Version: 1.0 
Release: 1
Summary: Virtual Machine Viewer
Group: Applications/System
License: GPLv2+
URL: http://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz
Requires: openssh-clients
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils


BuildRequires: glib2-devel >= 2.22
BuildRequires: gtk3-devel >= 3.10.0 
BuildRequires: spice-gtk-devel >= 0.20
BuildRequires: spice-protocol >= 0.10.1
BuildRequires: gtk-vnc-devel

%description
Virtual Machine Viewer provides a graphical console client for connecting
to virtual machines. It uses the GTK-VNC or SPICE-GTK widgets to provide
the display, and libvirt for looking up VNC/SPICE server details.

%prep
%setup -q

%build
export CC=clang
export CXX=clang++

%configure \
    --with-spice-gtk \
    --with-gtk-vnc \
    --with-gtk=3.0 \
    --disable-update-mimedb

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install  DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_libexecdir}
install -D -m 0755 data/spice-xpi-client-remote-viewer %{buildroot}%{_libexecdir}/spice-xpi-client

#no icon in desktop file.
echo "Icon=virt-viewer" >> $RPM_BUILD_ROOT/%{_datadir}/applications/remote-viewer.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database -q %{_datadir}/applications ||:
update-mime-database /usr/share/mime ||:

%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q %{_datadir}/applications ||:
update-mime-database /usr/share/mime ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/remote-viewer
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ui/
%{_datadir}/%{name}/ui/virt-viewer.xml
%{_datadir}/%{name}/ui/virt-viewer-auth.xml
%{_datadir}/%{name}/ui/virt-viewer-about.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/remote-viewer.desktop
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_libexecdir}/spice-xpi-client
%{_datadir}/icons/hicolor/*/devices/virt-viewer-usb.svg
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*

%changelog
