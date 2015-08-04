%define po_package libgtop-2.0

Name:     libgtop2
Summary:  LibGTop library (version 2)
Version:  2.30.0
Release:  1 
License:  GPLv2+
URL:      http://download.gnome.org/sources/libgtop/2.28
Group:    System Environment/Libraries
#VCS: git://git.gnome.org/libgtop
Source:   http://download.gnome.org/sources/libgtop/2.28/libgtop-%{version}.tar.xz
Patch0:   libgtop-fix-header.patch
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libtool gettext
BuildRequires:  intltool libtool

%description
LibGTop is a library for portably obtaining information about processes,
such as their PID, memory usage, etc.

%package devel
Summary:  Libraries and include files for developing with libgtop
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with LibGTop.

%prep
%setup -q -n libgtop-%{version}
%patch0 -p1

%build
%configure --disable-gtk-doc --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GTop-2.0.typelib

%files devel
%{_libdir}/*.so
%{_includedir}/libgtop-2.0
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GTop-2.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libgtop
# not worth fooling with
%exclude %{_datadir}/info

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

