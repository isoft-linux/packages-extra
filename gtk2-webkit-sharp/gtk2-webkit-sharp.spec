Name:           gtk2-webkit-sharp
Summary:        WebKit GTK2 bindings for Mono
Version:        0.3 
Release:        5 
License:        LGPL v2.0 only; LGPL v2.0 or later
Url:            http://www.mono-project.org/

Source:         http://download.mono-project.com/sources/webkit-sharp/webkit-sharp-%{version}.tar.bz2
Patch0:         webkit-sharp-with-new-webkitgtk.patch

BuildRequires:  gtk2-sharp gtk2-sharp-gapi webkitgtk-gtk2-devel mono-devel
Requires:       webkitgtk-gtk2 gtk2-sharp

BuildArch:noarch
%description
WebKit is a web content engine, derived from KHTML and KJS from KDE, and used
primarily in Apple's Safari browser. It is made to be embedded in other
applications, such as mail readers, or web browsers.

This package provides Mono bindings for WebKit GTK2 libraries.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-sharp gtk2-sharp-gapi

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n webkit-sharp-%{version}
%patch0 -p1

%build
autoreconf
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -D -m 0644 samples/funnybrowser.exe $RPM_BUILD_ROOT/%{_bindir}/funnybrowser-gtk2.exe 
%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root)
%{_bindir}/funnybrowser-gtk2.exe
%{_libdir}/mono/gac/webkit-sharp
%{_libdir}/mono/webkit-sharp

%files devel
%{_libdir}/monodoc/sources/webkit-sharp-docs*
%{_libdir}/pkgconfig/webkit-sharp-1.0.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.3-5
- Rebuild

