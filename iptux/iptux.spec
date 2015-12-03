%define bugfix 2
Name:           iptux
Version:        0.5.1
Release:        17
Summary:        A software for sharing in LAN
License:        GPLv2+
URL:            http://code.google.com/p/iptux/
Source0:        http://iptux.googlecode.com/files/%{name}-%{version}-%{?bugfix}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  GConf2-devel, gtk2-devel, desktop-file-utils
BuildRequires:  gettext, dbus-devel, gstreamer-devel

%description
A software for sharing and transporting files and
directories in LAN. It is written by C++ and the
skin is designed by gtk. Iptux is based on ipmsg,
so you can use it send files to a Windows PC which
has an ipmsg Windows edition in Lan.


%prep
%setup -q -n %{name}-%{version}


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
%find_lang %{name}
desktop-file-install \
  --delete-original \
  --dir ${RPM_BUILD_ROOT}/%{_datadir}/applications \
  ${RPM_BUILD_ROOT}/%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog style
%{_bindir}/%{name}
%{_bindir}/ihate%{name}
%{_datadir}/applications/iptux.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/64x64/apps/i-tux.png
%{_datadir}/icons/hicolor/64x64/apps/ip-tux.png
%{_datadir}/icons/hicolor/16x16/apps/i-tux.png
%{_datadir}/icons/hicolor/16x16/apps/ip-tux.png
%{_datadir}/icons/hicolor/22x22/apps/i-tux.png
%{_datadir}/icons/hicolor/22x22/apps/ip-tux.png
%{_datadir}/icons/hicolor/24x24/apps/i-tux.png
%{_datadir}/icons/hicolor/24x24/apps/ip-tux.png
%{_datadir}/icons/hicolor/32x32/apps/i-tux.png
%{_datadir}/icons/hicolor/32x32/apps/ip-tux.png
%{_datadir}/icons/hicolor/48x48/apps/i-tux.png
%{_datadir}/icons/hicolor/48x48/apps/ip-tux.png

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.5.1-17
- update release

* Wed Dec 02 2015 sulit <sulitsrc@gmail.com> - 0.5.1-16
- Init for isoft4
