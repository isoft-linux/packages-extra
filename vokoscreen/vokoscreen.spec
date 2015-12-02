Summary: Screencasting
Name: vokoscreen
Version: 2.4.8
Release: 4 
License: GPL-2.0
URL: http://www.kohaupt-online.de/hp
#https://github.com/vkohaupt/vokoscreen
Source0: vokoscreen-%{version}-beta.tar.gz

#Updated zh CN translation
Source1: vokoscreen_zh_CN.ts

#Patch0: we-do-not-have-mp3lame.patch
Patch1: vokoscreen-add-our-bomi-player.patch
Patch2: vokoscreen-really-quit.patch
Patch3: vokoscreen-update-hide-show-window-status.patch
Patch4: vokoscreen-add-zh_CN-info-to-desktop.patch
Patch5: vokoscreen-disable-check-new-version.patch
Patch6: vokoscreen-change-window-title.patch
 
Requires: ffmpeg 
Requires: bomi

BuildRequires: qt5-qtbase-devel qt5-qtx11extras-devel qt5-qttools-devel

BuildRequires: libXrandr-devel

BuildRequires: alsa-lib-devel libv4l-devel

%description
vokoscreen is an easy to use screencast creator to record educational videos,
live recordings of browser, installation, videoconferences, etc.

%prep
%autosetup -n %{name}-%{version}-beta -p1
rm -rf language/vokoscreen_zh_CN.ts
cp %{SOURCE1} language
 
%build
qmake-qt5
make %{?_smp_mflags}

%install
install -D -m 755 vokoscreen %{buildroot}%{_bindir}/vokoscreen
install -D -m 644 applications/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -m 644 applications/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m 644 man/man1/%{name}.1.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%files
%defattr(-, root, root)
%{_bindir}/vokoscreen
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.gz

%changelog
* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 2.4.8-4
- Restore mp3lame support

* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 2.4.8-3
- Rebuilt

* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 2.4.8-2
- Update to 2.4.8 Beta
- Add our fixes(a lot of)
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4.3-2.git
- Rebuild
