Summary: Extra image decoders.  
Name: evas_generic_loaders
Version: 1.15.0
Release: 2 
License: LGPLv2.1 GPLv2.1 BSD
Group: System Environment/Libraries
URL: http://www.enlightenment.org/
Source: http://download.enlightenment.org/releases/%{name}-%{version}.tar.gz

BuildRequires: poppler-devel, libspectre-devel, efl-devel, librsvg2-devel 
BuildRequires: gstreamer-devel >= 1.0
BuildRequires: gstreamer-plugins-base-devel >= 1.0

%description
These are additional "generic" loaders for Evas that are stand-alone
executables that evas may run from its generic loader module. This
means that if they crash, the application loading the image does not
crash also. In addition the licensing of these binaries will not
affect the license of any application that uses Evas as this uses a
completely generic execution system that allows anything to be plugged
in as a loader.

%package devel
Summary:headers, static libraries, documentation and test programs
Group: System Environment/Libraries
Requires: %{name} = %{version}

%description devel
Headers, static libraries, test programs and documentation.


%prep
%setup -q

%build
export CC=clang
export CXX=clang++
#./autogen.sh
%configure

make %{?_smp_mflags}
#make doc

%install
make DESTDIR=$RPM_BUILD_ROOT install

rpmclean
%clean
test "x$RPM_BUILD_ROOT" != "x/" && rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%defattr(-, root, root)
%{_libdir}/evas/utils/evas_*

%changelog
* Tue Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update to 1.15.0
