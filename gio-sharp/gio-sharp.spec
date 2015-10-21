Name:           gio-sharp
Summary:        gio bindings for Mono
Version:        2.22.3
Release:        4 
License:        LGPL v2.0 only; LGPL v2.0 or later
Group:          Development/Libraries
Url:            http://www.go-mono.org/

Source:         %{name}-%{version}.tar.bz2

BuildRequires:  gtk2-sharp gtk2-sharp-gapi mono
Requires:       gtk2-sharp

%description
gio bindings for Mono

%prep
%setup -q -n %{name}-%{version} -q
%build
%configure
make CSC=dmcs 

%install
make install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf "$RPM_BUILD_ROOT"
%files
%defattr(-, root, root)
/usr
