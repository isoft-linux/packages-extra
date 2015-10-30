%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}

Name:           itcl
Version:        4.0.3
Release:        4%{?dist}
Summary:        Object oriented extensions to Tcl and Tk

License:        TCL
URL:            http://incrtcl.sourceforge.net/itcl/
Source0:        https://downloads.sourceforge.net/incrtcl/itcl%{version}.tar.gz
Patch1:         itcl-libdir.patch
Patch2:         itcl-soname.patch

Requires:       tcl(abi) = 8.6
BuildRequires:  tcl-devel >= 1:8.6

%description
[incr Tcl] is Tcl extension that provides object-oriented features that are
missing from the Tcl language.

%package devel
Summary:  Development headers and libraries for linking against itcl
Requires:       %{name} = %{version}-%{release}
%description devel
Development headers and libraries for linking against itcl.

%prep
%setup -q -n %{name}%{version}
%patch1 -p1 -b .libdir
%patch2 -p1 -b .soname

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Patch the updated location of the stub library
sed -i -e "s#%{_libdir}/%{name}%{version}#%{tcl_sitearch}/%{name}%{version}#" \
        $RPM_BUILD_ROOT%{_libdir}/itclConfig.sh

%check
make test


%files
%dir %{tcl_sitearch}/%{name}%{version}
%{tcl_sitearch}/%{name}%{version}/*.tcl
%{_libdir}/*.so
%{_mandir}/mann/*.gz
%doc license.terms

%files devel
%{_includedir}/*.h
%{tcl_sitearch}/%{name}%{version}/*.a
%{_libdir}/itclConfig.sh

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.0.3-4
- Rebuild

