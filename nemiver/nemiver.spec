Name:	    nemiver	
Version:    0.9.6
Release:	2.git
Summary:    standalone C/C++ debugger
    
License:	GPL
URL:		http://www.gnome.org
Source0:	%{name}.tar.gz
BuildRequires: boost-devel
BuildRequires: gtksourceviewmm-devel
BuildRequires: gdlmm-devel
BuildRequires: ghex-devel
BuildRequires: libgtop2-devel

BuildRequires: pkgconfig(vte-2.91) 

%description
Nemiver is an on going effort to write an easy to use standalone C/C++ debugger that integrates well in the GNOME environment. 

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
%description devel
Nemiver is a standalone graphical debugger that integrates well in the
GNOME desktop environment. It currently features a backend which uses
the well known GNU Debugger gdb to debug C / C++ programs.

This package contains the development files to build debugger backend.

%prep
%setup -q -n %{name}
#sed -i 's@help@@g' Makefile.am

%build
export CC=cc
export CXX=c++
export CXXFLAGS="-std=c++11"

intltoolize 
autoreconf -ivf
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%find_lang nemiver 


%post
update-desktop-database -q> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  /usr/bin/gtk3-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
glib-compile-schemas /usr/share/glib-2.0/schemas/ >/dev/null 2>&1 ||:

%postun
update-desktop-database -q> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  /usr/bin/gtk3-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
glib-compile-schemas /usr/share/glib-2.0/schemas/ >/dev/null 2>&1 ||:

%files -f nemiver.lang
%{_bindir}/nemiver
%{_libdir}/nemiver
%{_datadir}/applications/nemiver.desktop
%{_datadir}/glib-2.0/schemas/org.nemiver.gschema.xml
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/help/*/nemiver
%{_datadir}/icons/hicolor/*/apps/nemiver*
%{_datadir}/nemiver
%{_mandir}/man1/nemiver.1.gz

%files devel
%{_includedir}/nemiver

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.9.6-2.git
- Rebuild

