Summary: GNUstep GUI Library 
Name: gnustep-gui
Version: 0.24.1
Release: 2
Source: http://ftpmain.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
License: see COPYING
BuildRequires: clang 
BuildRequires: gnustep-make 
BuildRequires: libobjc2-devel
BuildRequires: gnustep-base-devel
#build gnustep-back depend on gnustep-gui
#but gnustep-gui need gnustep-back installed to display widgets correctly.
Requires: gnustep-back

%description
The GNUstep gui library is a library of graphical user interface classes
written completely in the Objective-C language; the classes are based
upon Apple's Cocoa framwork (which came from the OpenStep
specification).  These classes include graphical objects such as
buttons, text fields, popup lists, browser lists, and windows; there
are also many associated classes for handling events, colors, fonts,
pasteboards and images.

%package devel
Summary: Development tools for gnustep-gui
Requires: %{name} = %{version}-%{release}

%description devel
The gnustep-gui-devel package contains header files and documentation necessary
for developing programs using gnustep.

%prep
%setup

%build
%configure CC=clang CXX=clang++ 
make CC=clang CXX=clang++

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) 
%doc COPYING README
%{_bindir}/gclose
%{_bindir}/gcloseall
%{_bindir}/gopen
%{_bindir}/make_services
%{_bindir}/set_show_service
%dir %{_libdir}/GNUstep/ColorPickers
%ghost %{_libdir}/GNUstep/Fonts
%dir %{_libdir}/GNUstep/Images
%dir %{_libdir}/GNUstep/KeyBindings
%dir %{_libdir}/GNUstep/PostScript
%dir %{_libdir}/GNUstep/Services
%dir %{_libdir}/GNUstep/Themes
%dir %{_libdir}/GNUstep/Sounds
%{_libdir}/GNUstep/ColorPickers/*
%{_libdir}/GNUstep/Images/*
%{_libdir}/GNUstep/KeyBindings/*
%{_libdir}/GNUstep/PostScript/*
%{_libdir}/GNUstep/Services/*
%{_libdir}/GNUstep/Sounds/*
%dir %{_libdir}/GNUstep/Libraries/gnustep-gui
%{_libdir}/GNUstep/Libraries/gnustep-gui/*
%{_libdir}/GNUstep/Bundles/*
%{_libdir}/*.so.*

%files devel
%attr(-,root,root)
%{_datadir}/GNUstep/Makefiles/Additional/gui.make
%{_libdir}/*.so
%dir %{_includedir}/AppKit
%{_includedir}/AppKit/*
%dir %{_includedir}/Cocoa
%{_includedir}/Cocoa/*
%dir %{_includedir}/GNUstepGUI
%{_includedir}/GNUstepGUI/*
%dir %{_includedir}/gnustep/gui
%{_includedir}/gnustep/gui/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.24.1-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

