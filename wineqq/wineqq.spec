Name: wineqq
Version: 6.7
Release: 4
Summary: Wine QQ Light Edition

License: Commercial
URL: http://www.qq.com
#refer to readme about 'how to create it'.
Source0: QQLite-%{version}.tar.xz

Source10: qq
Source20: wine-qq.desktop
Source21: qq.png

BuildRequires: p7zip p7zip-plugins
Requires: wine32

%description
Wine QQ Light

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}/QQLite
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
mkdir -p %{buildroot}%{_bindir}
tar Jxf %{SOURCE0} -C %{buildroot}%{_datadir}/QQLite --strip-component=1 

#we need copy QQLite to ~/.local
#so we have to add a file here to detect whether ~/.local/QQLite is outdated or not after update.
#create update indicator file
echo "%{version}-%{release}" >%{buildroot}%{_datadir}/QQLite/ver

install -m0755 %{SOURCE10} %{buildroot}%{_bindir}
install -m0644 %{SOURCE20} %{buildroot}%{_datadir}/applications
install -m0644 %{SOURCE21} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_bindir}/qq
%{_datadir}/QQLite
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/applications/*.desktop

%changelog
* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 6.7-4
- Update source, remove qqloginfix, we hack it in wine now.

* Tue Dec 01 2015 Cjacker <cjacker@foxmail.com> - 6.7-3
- Add qqloginfix to tarball

* Mon Nov 30 2015 Cjacker <cjacker@foxmail.com> - 6.7-2
- Initial build

