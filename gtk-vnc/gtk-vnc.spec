Summary: A GTK2 widget for VNC clients
Name: gtk-vnc
Version: 0.5.4
Release: 3
License: LGPLv2+
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.5/%{name}-%{version}.tar.xz
URL: http://live.gnome.org/gtk-vnc
BuildRequires: gtk3-devel >= 3.0 
BuildRequires: libtool
BuildRequires: gobject-introspection-devel

%description
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package devel
Summary: Development files to build GTK2 applications with gtk-vnc
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel

%description devel
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%package python
Summary: Python bindings for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description python
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

A module allowing use of the GTK-VNC widget from python

%package -n gvnc
Group: Development/Libraries
Summary: A GObject for VNC connections

%description -n gvnc
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

%package -n gvnc-devel
Summary: Libraries, includes, etc. to compile with the gvnc library
Group: Development/Libraries
Requires: gvnc = %{version}-%{release}
Requires: pkgconfig

%description -n gvnc-devel
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

Libraries, includes, etc. to compile with the gvnc library

%package -n gvnc-tools
Summary: Command line VNC tools
Group: Applications/Internet

%description -n gvnc-tools
Provides useful command line utilities for interacting with
VNC servers. Includes the gvnccapture program for capturing
screenshots of a VNC desktop

%package -n gtk-vnc2
Summary: A GTK3 widget for VNC clients
Group: Applications/Internet

%description -n gtk-vnc2
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package -n gtk-vnc2-devel
Summary: Development files to build GTK3 applications with gtk-vnc
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel

%description -n gtk-vnc2-devel
gtk-vnc is a VNC viewer widget for GTK3. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%prep
%setup -q 

%build
export CC=clang
export CXX=clang++

%configure --with-gtk=3.0 --enable-introspection --disable-plugin --without-python --without-sasl
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{name}

rpmclean
%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libgtk-vnc-2.0.so.*
%{_libdir}/girepository-1.0/GtkVnc-2.0.typelib

%files devel
%defattr(-, root, root)
%doc gtk-vnc2-%{version}/examples/gvncviewer.c
%{_libdir}/libgtk-vnc-2.0.so
%dir %{_includedir}/%{name}-2.0/
%{_includedir}/%{name}-2.0/*.h
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_datadir}/gir-1.0/GtkVnc-2.0.gir
%{_datadir}/vala/vapi/*

#%files python
#%defattr(-, root, root)
#%doc gtk-vnc-%{version}/examples/gvncviewer.py
#%{_libdir}/python*/site-packages/gtkvnc.so

%files -n gvnc -f %{name}.lang
%defattr(-, root, root)
%{_libdir}/libgvnc-1.0.so.*
%{_libdir}/libgvncpulse-1.0.so.*

%{_libdir}/girepository-1.0/GVnc-1.0.typelib
%{_libdir}/girepository-1.0/GVncPulse-1.0.typelib



%files -n gvnc-devel
%defattr(-, root, root)
%{_libdir}/libgvnc-1.0.so
%{_libdir}/libgvncpulse-1.0.so
%dir %{_includedir}/gvnc-1.0/
%{_includedir}/gvnc-1.0/*.h
%dir %{_includedir}/gvncpulse-1.0/
%{_includedir}/gvncpulse-1.0/*
%{_libdir}/pkgconfig/gvnc-1.0.pc
%{_libdir}/pkgconfig/gvncpulse-1.0.pc
%{_datadir}/gir-1.0/GVnc-1.0.gir
%{_datadir}/gir-1.0/GVncPulse-1.0.gir

%files -n gvnc-tools
%defattr(-, root, root)
%{_bindir}/gvnccapture
%{_mandir}/man1/gvnccapture.1*


%changelog
