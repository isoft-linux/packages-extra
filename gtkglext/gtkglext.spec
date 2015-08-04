%define api_version		1.0

Summary:	OpenGL Extension to GTK
Name:		gtkglext
Version:	1.2.0
Release:	25%{?dist}

License:	LGPLv2+ or GPLv2+
Group:		System Environment/Libraries
URL:		http://gtkglext.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/gnome/sources/gtkglext/1.2/gtkglext-%{version}.tar.bz2
# Upstream changes, addressing BZ 677457
Patch0:		gtkglext-1.2.0-bz677457.diff
# config.{sub,guess} from automake-1.13.4, addressing BZ 925512
Patch1:		gtkglext-1.2.0-config.diff

BuildRequires:	gtk2-devel
BuildRequires:	libGLU-devel
BuildRequires:	libGL-devel
# Conditional build feature
BuildRequires:	libXmu-devel
# The configure script checks for X11/Intrinsic.h
BuildRequires:	libXt-devel
BuildRequires:  pangox-compat-devel

Requires(postun):	/sbin/ldconfig
Requires(post):		/sbin/ldconfig

%description
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%package libs
Summary:	OpenGL Extension to GTK
Group:		System Environment/Libraries
License:	LGPLv2+

%description libs
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%package devel
Summary:	Development tools for GTK-based OpenGL applications
Group:		Development/Libraries
License:	LGPLv2+

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	gtk2-devel
Requires:	libGL-devel
Requires:	libGLU-devel
Requires:	libXmu-devel

%description devel
The gtkglext-devel package contains the header files, static libraries,
and developer docs for GtkGLExt.

%prep
%setup -q -n gtkglext-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure --disable-gtk-doc --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files libs
%doc AUTHORS COPYING COPYING.LIB ChangeLog README TODO
%{_libdir}/libgdkglext-x11-%{api_version}.so.*
%{_libdir}/libgtkglext-x11-%{api_version}.so.*

%files devel
%{_includedir}/*
%{_libdir}/gtkglext-%{api_version}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
%doc %{_datadir}/gtk-doc/html/*

%changelog
