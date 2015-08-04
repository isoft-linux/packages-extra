Name:		phodav
Version:	2.0
Release:	1
Summary:	phodav is a WebDav server implementation using libsoup (RFC 4918). 

Group:	    Framework/Utilities	
License:	GPL
URL:		https://wiki.gnome.org/phodav
Source0:	http://ftp.gnome.org/pub/GNOME/sources/phodav/2.0/phodav-2.0.tar.xz

BuildRequires:  libsoup-devel	
Requires:	libsoup
Requires:   lib%{name} = %{version}-%{release}

%description
%{summary}

%package -n libphodav 
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description -n libphodav
%{summary}

%package -n libphodav-devel 
Summary:        Development files for lib%{name}
Group:          Development/Libraries
Requires:       lib%{name} = %{version}-%{release}

%description -n libphodav-devel
The lib%{name}-devel package contains libraries and header files for
developing applications that use lib%{name}.

%package -n spice-webdavd
Summary: Spice webdavd
Group: Applications/Internet

%description -n spice-webdavd
Spice webdavd

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%find_lang phodav

%files -f phodav.lang
%{_bindir}/chezdav
%{_mandir}/man1/chezdav.1.gz

%files -n libphodav
%{_libdir}/libphodav-*.so.*

%files -n libphodav-devel
%{_includedir}/libphodav-2.0
%{_libdir}/libphodav-*.so
%{_libdir}/pkgconfig/libphodav-*.pc
%{_datadir}/gtk-doc/html/phodav


%files -n spice-webdavd
%{_sbindir}/spice-webdavd
%{_libdir}/systemd/system/spice-webdavd.service
%{_libdir}/udev/rules.d/70-spice-webdavd.rules

%changelog

