Summary: GTK theme for GNUstep
Name: gnustep-plugins-themes-gtk
Version: 20140115 
Release: 1
Source: ftp://ftp.gnustep.org/pub/gnustep/core/%{name}.tar.gz
Group:  System Environment/Libraries 
License: see COPYING
BuildRequires: clang 
BuildRequires: libobjc2-devel
BuildRequires: gnustep-make
BuildRequires: gnustep-base-devel
BuildRequires: gnustep-gui-devel
BuildRequires: gtk2-devel
BuildRequires: GConf2-devel

%description
Gnome is a theme engine for GNUstep which
uses the current Gtk+-Theme selected in Gnome
for drawing its widgets.

%prep
%setup -n %{name}

%build
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%doc COPYING README
%dir %{_libdir}/GNUstep/Themes/Gtk.theme
%{_libdir}/GNUstep/Themes/Gtk.theme/*
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

