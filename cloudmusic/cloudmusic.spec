Name: cloudmusic 
Version: 1.9.2
Release: 3
Summary: Netease Cloud Music

License: CloseSource But Free
URL: http://music.163.com/discover/ 
Source0: %{name}-%{version}.tar.xz 
#wrapper script.
Source10: cloudmusic
Source11: cloudmusic.desktop

Source12: cloudmusic-16.png  
Source13: cloudmusic-32.png  
Source14: cloudmusic-48.png
Source15: cloudmusic-256.png  

Patch1: system-reg-remove-xml.patch

Requires: wine32 

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,256x256}/apps

tar Jxf %{SOURCE0} -C %{buildroot}%{_datadir}
mv %{buildroot}%{_datadir}/%{name}-%{version} %{buildroot}%{_datadir}/%{name}
patch -p1 -i %{PATCH1} %{buildroot}%{_datadir}/%{name}/system.reg

install -m0755 %{SOURCE10} %{buildroot}%{_bindir}/

install -m0644 %{SOURCE11} %{buildroot}%{_datadir}/applications/

install -m0644 %{SOURCE12} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/cloudmusic.png
install -m0644 %{SOURCE13} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/cloudmusic.png
install -m0644 %{SOURCE14} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/cloudmusic.png
install -m0644 %{SOURCE15} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/cloudmusic.png


%files
%{_bindir}/cloudmusic
%{_datadir}/cloudmusic
%{_datadir}/applications/cloudmusic.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Mon Jan 11 2016 xiaotian.wu@i-soft.com.cn - 1.9.2-3
- remove xml file associations to fix bug 13240.

* Thu Dec 03 2015 Cjacker <cjacker@foxmail.com> - 1.9.2-2
- Initial build


