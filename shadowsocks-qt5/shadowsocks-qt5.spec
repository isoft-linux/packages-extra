Name: shadowsocks-qt5
Version: 2.5.1
Release: 2
Summary: A cross-platform shadowsocks GUI client	

License: GPL
URL: https://github.com/librehat/shadowsocks-qt5	
#git clone https://github.com/librehat/shadowsocks-qt5
Source0: %{name}-%{version}.tar.gz 
Source1: libQtShadowsocks-1.7.0.tar.gz
Source2: zbar-0.10.tar.bz2

#we treat libQtShadowsocks/libzbar as private and internal used library of shadowsocks-qt5
#so we install it in a private dir and use rpath.
Patch0: shadowsocks-qt5-change-rpath-to-private-dir.patch
BuildRequires: qt5-qtbase-devel	

%{?filter_setup:
%filter_provides_in /usr/lib/shadowsocks-qt5
%filter_requires_in /usr/bin
%filter_setup
}
Requires: botan libappindicator qt5-qtbase 
%description
%{summary}

%prep
%setup -q -a1 -a2
%patch0 -p1

%build
pushd libQtShadowsocks-1.7.0
qmake-qt5
make %{?_smp_mflags}
make install INSTALL_ROOT=`pwd`/../internal-bin
popd

interlnal_usr=`pwd`/internal-bin/usr
sed -i 's|prefix=/usr|prefix='"$interlnal_usr"'|g' internal-bin/usr/lib/pkgconfig/QtShadowsocks.pc

pushd zbar-0.10
./configure --prefix=`pwd`/../internal-bin/usr --disable-video
make %{?_smp_mflags}
make install
popd

export PKG_CONFIG_PATH=`pwd`/internal-bin/usr/lib/pkgconfig
export CXXFLAGS="-Wl, -rpath=/usr/lib/shadowsocks-qt5"
qmake-qt5
make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}


mkdir -p %{buildroot}%{_libdir}/shadowsocks-qt5

install -m 0755 internal-bin/usr/lib/libQtShadowsocks.so.* %{buildroot}%{_libdir}/shadowsocks-qt5 
install -m 0755 internal-bin/usr/lib/libzbar.so.* %{buildroot}%{_libdir}/shadowsocks-qt5 

%files
%{_bindir}/ss-qt5
%{_libdir}/shadowsocks-qt5
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.5.1-2
- Rebuild

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 2.5.1
- long live shadowsocks.

* Sun Aug 16 2015 Cjacker <cjacker@foxmail.com>
- add rpath patch, support search libs in private dir.
