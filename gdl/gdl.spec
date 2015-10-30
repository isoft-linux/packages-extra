Name:           gdl
Version:        3.16.0
Release:        2
Summary:        Gnome Development Library 
License:        GPLv2+
Source0:        http://ftp.acc.umu.se/pub/GNOME/sources/gdl/3.16/%{name}-%{version}.tar.xz
BuildRequires:  gobject-introspection
%description
GDL is the Gnome Development Library. It features a docking system and can also be used without any gnome dependency

%package devel
Summary: Headers and libraries for using gdl

%description devel
This package contains headers and libraries to develop program with gdl.
%prep
%setup -q -n %{name}-%{version}
%build
export CC=clang
export CXX=clang++
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gdl-3

%clean
rm -rf $RPM_BUILD_ROOT


%files -f gdl-3.lang
%{_libdir}/girepository-1.0/Gdl-3.typelib
%{_libdir}/libgdl-3.so.*

%files devel
%dir %{_includedir}/libgdl-3.0
%{_includedir}/libgdl-3.0/*
%{_libdir}/libgdl-3.so
%{_libdir}/pkgconfig/gdl-3.0.pc
%{_datadir}/gir-1.0/Gdl-3.gir
%dir %{_datadir}/gtk-doc/html/gdl-3.0
%{_datadir}/gtk-doc/html/gdl-3.0/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.16.0-2
- Rebuild

