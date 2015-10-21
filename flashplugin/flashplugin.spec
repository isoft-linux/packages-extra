Summary: Flash Player Plugin for FireFox and Other browsers 
Name: flashplugin 
Version: 11.2.202.521
Release: 3 
URL:    https://www.adobe.com/support/flashplayer/downloads.html
Source0: install_flash_player_11_linux.x86_64.tar.gz 
#kde4 is outdated, there is no systemsettings module for kde5, so we use kcmshell4 to launch it
Source1: kde-flash-panel.desktop

#add to systemsettings5 as external app.
Source2: flash.desktop

Group: Applications/Multimedia
License:Commecial

%description
Flash Player Plugin for FireFox 

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins
tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT
mv  $RPM_BUILD_ROOT/libflashplayer.so  $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins

rm -rf $RPM_BUILD_ROOT/readme.txt
rm -rf $RPM_BUILD_ROOT/usr/lib/kde4/kcm_adobe_flash_player.so
mv  $RPM_BUILD_ROOT/usr/lib64/kde4/kcm_adobe_flash_player.so $RPM_BUILD_ROOT/usr/lib/kde4/
#rm -rf $RPM_BUILD_ROOT/usr/share/kde4/services/kcm_adobe_flash_player.desktop

#rm -rf usr/lib
#mv usr/lib64 usr/lib

#tar cf kcm.tar usr
#tar xf kcm.tar -C $RPM_BUILD_ROOT

#change category in systemsettings 
#sed -i 's/personal/system-administration/g' $RPM_BUILD_ROOT/%{_datadir}/kde4/services/kcm_adobe_flash_player.desktop
chmod 644 $RPM_BUILD_ROOT%{_datadir}/applications/flash-player-properties.desktop

cat >>$RPM_BUILD_ROOT%{_datadir}/applications/flash-player-properties.desktop <<EOF
Categories=GNOME;GTK;Settings;X-GNOME-SystemSettings;X-GNOME-Settings-Panel;
OnlyShowIn=GNOME;Unity;
NoDisplay=true
Keywords=flash;plugin;
EOF

mv $RPM_BUILD_ROOT%{_datadir}/applications/flash-player-properties.desktop $RPM_BUILD_ROOT%{_datadir}/applications/gnome-flash-panel.desktop

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications/kde-flash-panel.desktop

#install systemsettings5 entry.
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/kservices5/flash.desktop
 
%clean
rm -rf $RPM_BUILD_ROOT

%post
kbuildsycoca4 >/dev/null 2>&1 ||:

%postun
kbuildsycoca4 >/dev/null 2>&1 ||:

%files
%defattr(-,root,root)
%{_bindir}/flash-player-properties
%{_libdir}/kde4/kcm_adobe_flash_player.so
%{_libdir}/mozilla/plugins/libflashplayer.so
%{_datadir}/applications/gnome-flash-panel.desktop
%{_datadir}/applications/kde-flash-panel.desktop
%{_datadir}/kservices5/flash.desktop
#%{_datadir}/applications/flash-player-properties.desktop
%{_datadir}/icons/hicolor/*/apps/flash-player-properties.png
%{_datadir}/kde4/services/kcm_adobe_flash_player.desktop
%{_datadir}/pixmaps/flash-player-properties.png

%changelog
* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- update to 521
