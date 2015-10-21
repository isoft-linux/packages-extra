Name:	    audacious	
Version:	3.7
Release:	1
Summary:	An Advanced Audio Player

License:    See license in source	
URL:		http://audacious-media-player.org/
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}-alpha1.tar.bz2
Patch0:     audacious-set-chardet-fallback-to-gbk.patch

BuildRequires: qt5-qtbase-devel	
Requires:	qt5-qtbase

%description
Audacious is an open source audio player. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}-alpha1
%patch0 -p1

%build
%configure \
    --disable-gtk \
    --enable-qt
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%find_lang audacious


%post
/sbin/ldconfig 
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi

%files -f audacious.lang
%{_bindir}/audacious
%{_bindir}/audtool
%{_libdir}/libaud*.so.*
%{_datadir}/applications/audacious.desktop
%{_datadir}/audacious/
%{_datadir}/icons/hicolor/*/apps/audacious.*
%{_mandir}/man1/audacious.1.gz
%{_mandir}/man1/audtool.1.gz

%files devel
%{_includedir}/audacious
%{_includedir}/libaudcore
%{_includedir}/libaudqt
#%{_includedir}/libaudgui
%{_libdir}/libaud*.so
%{_libdir}/pkgconfig/audacious.pc

%changelog


