Name:           gtk2-sharp
Version:        2.12.26
Release:        2
Summary:        GTK+ 2.0 bindings for Mono

License:        LGPL
URL:            http://www.mono-project.org
Source0:        http://download.mono-project.com/sources/gtk-sharp212/gtk-sharp-%{version}.tar.gz

BuildRequires:  mono gtk2-devel libglade2-devel
BuildRequires:  automake, libtool, mono

%description
This package provides a library that allows you to build
fully native graphical GNOME applications using Mono. Gtk#
is a binding to GTK+, the cross platform user interface
toolkit used in GNOME. It includes bindings for Gtk, Atk,
Pango, Gdk.

%package gapi
Summary:      Glib and GObject C binding generator for Mono.
Requires:     perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX
Requires:     %{name} = %{version}-%{release}

%description gapi
This package provides developer tools for the creation and
maintainance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk,
libgnome, libgnomeui and libgnomecanvas.

%package docs 
Summary:      gtk2 sharp documents 
Requires:     %{name} = %{version}-%{release}

%description docs 
This package provides documents for gtk2 Mono binding.

%prep
%setup -n gtk-sharp-%{version}

%build
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
make install DESTDIR=$RPM_BUILD_ROOT GACUTIL_FLAGS="/package gtk-sharp /gacdir %{_prefix}/lib /root ${RPM_BUILD_ROOT}%{_prefix}/lib"
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.*a
mv $RPM_BUILD_ROOT%{_prefix}/lib/mono/gtk-sharp $RPM_BUILD_ROOT%{_prefix}/lib/mono/gtk-sharp-2.0

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%dir %{_prefix}/lib/gtk-sharp-2.0
%{_prefix}/lib/mono/gac
%{_prefix}/lib/mono/gtk-sharp-2.0
%{_libdir}/pkgconfig/*-sharp-2.0.pc
%{_libdir}/pkgconfig/gtk-dotnet-2.0.pc

%files gapi
%defattr(-,root,root,-)
%{_bindir}/gapi2-codegen
%{_bindir}/gapi2-fixup
%{_bindir}/gapi2-parser
%{_prefix}/lib/gtk-sharp-2.0/gapi_codegen.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-fixup.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-parser.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi_pp.pl
%{_prefix}/lib/gtk-sharp-2.0/gapi2xml.pl
%{_libdir}/pkgconfig/gapi-2.0.pc
%{_prefix}/share/gapi-2.0

%files docs
%defattr(-,root,root,-)
%{_libdir}/monodoc/sources/gtk-sharp-docs.source
%{_libdir}/monodoc/sources/gtk-sharp-docs.tree
%{_libdir}/monodoc/sources/gtk-sharp-docs.zip


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.12.26-2
- Rebuild

