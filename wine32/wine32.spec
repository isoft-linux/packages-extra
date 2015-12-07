Name: wine32 
Version: 1.8
Release: 5 
Summary: A compatibility layer for windows applications

License: LGPLv2+ 
URL: http://www.winehq.org

#this is 32bit wine
Source0: wine-common-%{version}-%{release}.noarch.rpm
Source1: wine-core-%{version}-%{release}.i686.rpm
Source2: wine-alsa-%{version}-%{release}.i686.rpm
Source3: wine-arial-fonts-%{version}-%{release}.noarch.rpm
Source4: wine-capi-%{version}-%{release}.i686.rpm
Source5: wine-cms-%{version}-%{release}.i686.rpm
Source6: wine-filesystem-%{version}-%{release}.noarch.rpm
Source7: wine-openal-%{version}-%{release}.i686.rpm
Source8: wine-opencl-%{version}-%{release}.i686.rpm
Source9: wine-pulseaudio-%{version}-%{release}.i686.rpm
Source10: wine-ldap-%{version}-%{release}.i686.rpm
Source11: wine-desktop-%{version}-%{release}.noarch.rpm
Source12: wine-systemd-%{version}-%{release}.noarch.rpm

#Just put it here, it's build with "rpmbuild -ba wine.spec --target=i686"
Source19: wine-%{version}-%{release}.src.rpm
 
#wine mono
Source20: wine-mono-4.5.6-4.fc23.noarch.rpm
#wine gecko
Source21: mingw32-wine-gecko-2.40-1.fc24.noarch.rpm

AutoReqProv: no
Requires: lib32-runtime

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%prep
%build
%install
mkdir -p %{buildroot}
pushd %{buildroot}

rpm2cpio %{SOURCE0} | cpio -id 
rpm2cpio %{SOURCE1} | cpio -id 
rpm2cpio %{SOURCE2} | cpio -id 
rpm2cpio %{SOURCE3} | cpio -id 
rpm2cpio %{SOURCE4} | cpio -id 
rpm2cpio %{SOURCE5} | cpio -id 
rpm2cpio %{SOURCE6} | cpio -id 
rpm2cpio %{SOURCE7} | cpio -id 
rpm2cpio %{SOURCE8} | cpio -id 
rpm2cpio %{SOURCE9} | cpio -id 
rpm2cpio %{SOURCE10} | cpio -id
rpm2cpio %{SOURCE11} | cpio -id
rpm2cpio %{SOURCE12} | cpio -id

rpm2cpio %{SOURCE20} | cpio -id
rpm2cpio %{SOURCE21} | cpio -id

rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_mandir}/*.UTF-8

pushd %{buildroot}%{_bindir}
ln -s wine32 wine
ln -s wineserver32 wineserver
popd

#hide all menus
for i in %{buildroot}%{_datadir}/applications/*.desktop
do
echo "NoDisplay=True" >> $i
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_sysconfdir}/ld.so*/*.conf
%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_bindir}/*
%{_libdir}/*
%{_mandir}/man1/*
%{_datadir}/wine
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/Wine.directory
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%changelog
* Mon Dec 07 2015 Cjacker <cjacker@foxmail.com> - 1.8-5
- Update to 1.8 git, aka. 1.8 rc3, update wine-staging to match it

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 1.8-4
- Update to 1.8-4
- Hack winex11drv to fix QQ Login dialog input issue.

* Thu Dec 03 2015 Cjacker <cjacker@foxmail.com> - 1.7.55-5
- Correct mic support issue.

* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 1.7.55-4
- Backport pulseaudio fix from wine 1.8
- Hack winex11drv to handle special shadow window of netease cloudmusic.exe

* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 1.7.55-3
- Add localized font replacements, convert wine.inf to utf8-bom
