%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}

Name:           itk
Version:        4.0.1
Release:        2%{?dist}
Summary:        Object oriented extensions to Tk

Group:          Development/Libraries
License:        TCL
URL:            http://incrtcl.sourceforge.net/itcl/
Source0:        https://downloads.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
Patch0:         itk-libdir.patch
Patch1:         itk-soname.patch
Patch2:         itcl4.0.0-linuxloading.patch
Patch4:         itcl4.0.0-tolowercase.patch

Requires:       tcl(abi) = 8.6 itcl tk
BuildRequires:  tk-devel itcl-devel

%description
[incr Tk] is Tk extension that provides object-oriented features that are
missing from the Tk extension to Tcl.  The OO features provided by itk are
useful for building megawidgets.

%package devel
Summary:  Development headers and libraries for linking against itk
Group: Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description devel
Development headers and libraries for linking against itk.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1 -b .libdir
%patch1 -p1 -b .soname
%patch2 -p1 -b .linuxloading
%patch4 -p1 -b .tolowercase

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%{_libdir}/*.so
%dir %{tcl_sitearch}/itk%{version}
%{tcl_sitearch}/%{name}%{version}/*.tcl
%{tcl_sitearch}/%{name}%{version}/*.itk
%{tcl_sitearch}/%{name}%{version}/tclIndex
%{_mandir}/mann/*.gz
%doc license.terms

%files devel
%{_includedir}/*.h
# What happened to itk's stub library and itkConfig.sh?

%changelog
