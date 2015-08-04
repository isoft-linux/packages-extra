Name:           spice-gtk
Version:        0.29
Release:        1
Summary:        A GTK2 widget for SPICE clients

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://spice-space.org/page/Spice-Gtk
Source0:        http://www.spice-space.org/download/gtk/%{name}-%{version}.tar.bz2

BuildRequires: intltool
BuildRequires: spice-protocol >= 0.9.0
BuildRequires: usbredir-devel >= 0.3.1
BuildRequires: libusb-devel >= 1.0.9
BuildRequires: libgudev-devel
BuildRequires: pixman-devel openssl-devel libjpeg-turbo-devel
BuildRequires: celt051-devel pulseaudio-libs-devel
BuildRequires: zlib-devel
BuildRequires: libcacard-devel
BuildRequires: gtk-doc
BuildRequires: gtk3-devel
# Hack because of bz #613466
BuildRequires: libtool

BuildRequires: perl-Text-CSV
ExclusiveArch: %{ix86} x86_64

%description
Client libraries for SPICE desktop servers.

%package devel
Summary: Development files to build GTK2 applications with spice-gtk-2.0
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: spice-glib-devel = %{version}-%{release}
Requires: pkgconfig

%description devel
spice-gtk provides a SPICE viewer widget for GTK.

Libraries, includes, etc. to compile with the spice-gtk libraries

%package -n spice-glib
Summary: A GObject for communicating with Spice servers
Group: Development/Libraries

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Group: Development/Libraries
Requires: spice-glib = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries

%package python
Summary: Python bindings for the spice-gtk-2.0 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description python
SpiceClientGtk module provides a SPICE viewer widget for GTK2.

A module allowing use of the spice-gtk-2.0 widget from python

%package tools
Summary: Spice-gtk tools
Group: Applications/Internet

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
snappy is a tool to capture screen-shots of a SPICE desktop.

%prep
%setup -q 


%build
export CC=clang
export CXX=clang++

#add a minor version, virt-manager will fail otherwise.
sed -i "s@PACKAGE_VERSION='0.24'@PACKAGE_VERSION='0.29.0'@g" configure

%configure --with-gtk=3.0 --without-python --enable-usbredir
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} DATADIRNAME=share

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
%find_lang %{name}
rpmclean

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc spice-gtk-%{version}/AUTHORS
%doc spice-gtk-%{version}/COPYING
%doc spice-gtk-%{version}/README
%doc spice-gtk-%{version}/NEWS
%{_libdir}/libspice-client-gtk-*.so.*
%{_libdir}/girepository-1.0/SpiceClientGtk-*.typelib

%files devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-gtk-*.so
%{_includedir}/spice-client-gtk-*
%{_libdir}/pkgconfig/spice-client-gtk-*.pc
%{_datadir}/gir-1.0/SpiceClientGtk-*.gir

%files -n spice-glib -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/spice-client-glib-usb-acl-helper
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/libspice-controller.so.*
%{_libdir}/girepository-1.0/SpiceClientGLib-2.0.typelib
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy

%files -n spice-glib-devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-controller.so
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-controller/*
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%{_datadir}/vala/vapi/spice-protocol.vapi
%doc %{_datadir}/gtk-doc/html/*

#%files python
#%defattr(-,root,root,-)
#%{_libdir}/python*/site-packages/SpiceClientGtk.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/spicy
%{_bindir}/spicy-stats
%{_bindir}/spicy-screenshot

%changelog
