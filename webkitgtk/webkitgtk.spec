Name:		webkitgtk
Version:    2.4.9
Release:	1
Summary:	GTK+ Web content engine library
Group:		Development/Libraries
License:	LGPLv2+ and BSD
URL:		http://www.webkitgtk.org/

Source0:	http://www.webkitgtk.org/webkitgtk-%{version}.tar.xz
Patch0:    webkit-gtk-1.7.90-parallel-make-hack.patch

BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	enchant-devel
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	gperf
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk3-devel
BuildRequires:	libsoup-devel >= 2.27.4
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libxslt-devel
BuildRequires:	libXt-devel
BuildRequires:	pcre-devel
BuildRequires:	sqlite-devel
BuildRequires:  libsecret-devel
BuildRequires:	cairo-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:  libwebp-devel

#only build script need it
BuildRequires:  ruby
%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
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
rpmclean

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
