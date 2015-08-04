Name:           gtk3-sharp
Version:        2.99.4
Release:        1.git
Summary:        GTK3 bindings for Mono

Group:          System Environment/Libraries
License:        LGPL
URL:            https://github.com/mono/gtk-sharp/ 
Source0:        gtk-sharp.tar.gz
Patch0:         gtk-sharp-use-dmcs.patch

BuildRequires:  mono gtk3-devel
BuildRequires:  automake, libtool, mono

%description
This package provides a library that allows you to build
fully native graphical GNOME applications using Mono. Gtk#
is a binding to GTK+, the cross platform user interface
toolkit used in GNOME. It includes bindings for Gtk3, Atk,
Pango, Gdk

%package gapi
Group:        Development/Languages
Summary:      Glib and GObject C source parser and C generator for the creation and maintenance of managed bindings for Mono and .NET
Requires:     perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX

%description gapi
This package provides developer tools for the creation and
maintainance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk.

%package docs 
Group:        Development/Languages
Summary:      gtk sharp documents 
Requires:     %{name} = %{version} 

%description docs 
This package provides documents for gtk-sharp

%prep
%setup -n gtk-sharp -q
%patch0 -p1

%build
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
./autogen.sh
%configure
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
make install DESTDIR=$RPM_BUILD_ROOT GACUTIL_FLAGS="/package gtk-sharp-3.0 /gacdir %{_prefix}/lib /root ${RPM_BUILD_ROOT}%{_prefix}/lib"
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.*a


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_prefix}/lib/mono/gac
%{_prefix}/lib/mono/gtk-sharp-3.0
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/pkgconfig/gapi-3.0.pc

%files gapi
%defattr(-,root,root,-)
%{_bindir}/gapi3-codegen
%{_bindir}/gapi3-fixup
%{_bindir}/gapi3-parser
%{_prefix}/lib/gapi-3.0/*
%{_libdir}/pkgconfig/gapi-3.0.pc
%{_prefix}/share/gapi-3.0

%files docs
%defattr(-,root,root,-)
%{_libdir}/monodoc/sources/*
