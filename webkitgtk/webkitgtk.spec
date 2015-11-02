Name: webkitgtk
Version: 2.4.9
Release: 3
Summary: GTK+ Web content engine library
License: LGPLv2+ and BSD
URL: http://www.webkitgtk.org/

Source0: http://www.webkitgtk.org/webkitgtk-%{version}.tar.xz
Patch0: webkit-gtk-1.7.90-parallel-make-hack.patch

BuildRequires: clang
BuildRequires: bison flex perl python ruby gperf gawk
BuildRequires: pkgconfig
BuildRequires: coreutils
BuildRequires: libjpeg-turbo-devel libpng-devel libwebp-devel
BuildRequires: glib2-devel libicu-devel zlib-devel libxml2-devel pango-devel
BuildRequires: enchant-devel cairo-devel gtk2-devel
BuildRequires: libXt-devel libXrender-devel libXcomposite-devel libXdamage-devel
BuildRequires: gtk3-devel 
BuildRequires: pkgconfig(gl) pkgconfig(egl) pkgconfig(glesv2)
BuildRequires: gobject-introspection-devel libsoup-devel libsecret-devel freetype-devel
BuildRequires: harfbuzz-devel sqlite-devel libxslt-devel pkgconfig(geoclue-2.0)
BuildRequires: gstreamer-devel gstreamer-plugins-base-devel

BuildRequires: gtk-doc 
BuildRequires: make
BuildRequires: gettext
BuildRequires: chrpath
BuildRequires: pcre-devel

%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gtk3-devel
Provides:	WebKit-gtk-devel = %{version}-%{release}
Obsoletes:	WebKit-gtk-devel < %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export CC=clang
export CXX=clang++

%configure	\
    --enable-gtk-doc \
    --enable-introspection \
    --enable-jit \
    --disable-webkit2 \
    --with-gtk=3.0

mkdir -p DerivedSources/webkit
mkdir -p DerivedSources/WebCore
mkdir -p DerivedSources/ANGLE
mkdir -p DerivedSources/WebKit2/webkit2gtk/webkit2
mkdir -p DerivedSources/WebKit2
mkdir -p DerivedSources/webkitdom/
mkdir -p DerivedSources/InjectedBundle
mkdir -p DerivedSources/Platform

make -j1 all-built-sources-local
make %{?_smp_mflags} all-ltlibraries-local
make %{?_smp_mflags} all-programs-local
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%find_lang WebKitGTK-3.0

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f WebKitGTK-3.0.lang
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_libdir}/girepository-?.?/*
%{_datadir}/webkit*

%files  devel
%defattr(-,root,root,-)
%{_bindir}/jsc*
%{_includedir}/webkit*-*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-?.?/*
%{_datadir}/gtk-doc/*

%changelog
* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 2.4.9-3
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4.9-2
- Rebuild

