Summary: Screencasting
Name: vokoscreen
Version: 2.4.3
Release: 2.git
License: GPL-2.0
URL: http://www.kohaupt-online.de/hp
#https://github.com/vkohaupt/vokoscreen
Requires: ffmpeg 

BuildRequires: qt5-qtbase-devel alsa-lib-devel

Source: %{name}.tar.gz

%description
vokoscreen is an easy to use screencast creator to record educational
videos, live recordings of browser, installation, videoconferences, etc.

%prep
%setup -n %{name}

%build
qmake-qt5
make

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
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4.3-2.git
- Rebuild

* Sun Mar 21 2012 Volker Kohaupt <vkohaupt@freenet.de> 1.6.3
- new Version
