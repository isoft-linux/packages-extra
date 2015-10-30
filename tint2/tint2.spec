%define imlib2_version 1.4.6
Name:		tint2	
Version:	0.11
Release:  4 
Summary:	tint2 is a simple panel/taskbar intentionally made for openbox3
License:	GPLv2+
URL:		http://code.google.com/p/tint2/	
Source0:    tint2-%{version}.tar.bz2
Source1:	tint2.desktop
Source2:    tintrc.everest
Patch0:     tint2-fix-exec.patch
Patch1:     launcher_apps_dir-v2.patch

Source10:        http://downloads.sourceforge.net/enlightenment/imlib2-%{imlib2_version}.tar.bz2
Patch100:         imlib2-giflib5.patch

BuildRequires: cmake, gtk2-devel
%description
tint2 is a simple panel/taskbar intentionally made for openbox3

%prep
%setup -q -a10
%patch0 -p1
%patch1 -p0

pushd imlib2-%{imlib2_version}
%patch100 -p0
popd


%build
export PKG_CONFIG_PATH=`pwd`/interbin/lib/pkgconfig

pushd imlib2-%{imlib2_version}
CFLAGS="-fPIC" ./configure --prefix=`pwd`/../interbin --disable-shared --enable-static --without-id3 --without-gif
make %{?_smp_mflags}
make install
popd

mkdir make
pushd make
LDFLAGS+="-lX11 -lXext -lfreetype -ldl -lm -lxcb -lbz2 -lXau" cmake -DCMAKE_INSTALL_PREFIX=/usr -DENABLE_TINT2CONF=off -DENABLE_BATTERY=on ..
make %{?_smp_mflags}
popd

%install
pushd make
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
popd

#cp *rc0* $RPM_BUILD_ROOT%{_sysconfdir}/xdg/tint2
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/tint2/
mkdir -p $RPM_BUILD_ROOT/etc/xdg/autostart
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xdg/autostart/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/*
#%{_datadir}/%{name}/  
%{_datadir}/doc
%{_datadir}/man
#%{_datadir}/pixmaps/*
%{_datadir}/tint2/*

%{_sysconfdir}/xdg/tint2  
%{_sysconfdir}/xdg/autostart/*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.11-4
- Rebuild

