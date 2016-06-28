%define soversion 1
%define soname libdwarf.so.%{soversion}
%define sofullname libdwarf.so.%{soversion}.%{version}.0

Name:          libdwarf
Version:       20150915
Release:       2
Summary:       Library to access the DWARF Debugging file format 
Group:         Development/Libraries

License:       LGPLv2
URL:           http://www.prevanders.net/dwarf.html
Source0:       http://www.prevanders.net/%{name}-%{version}.tar.gz
Patch0:        libdwarf-shlib.patch

##BuildRequires: binutils-devel elfutils-libelf-devel
BuildRequires: binutils-devel libelfutils-devel

%package devel
Summary:       Library and header files of libdwarf
Group:         Development/Libraries
License:       LGPLv2
Requires:      %{name} = %{version}-%{release}

%package static
Summary:       Static libdwarf library
Group:         Development/Libraries
License:       LGPLv2
Requires:      %{name}-devel = %{version}-%{release}

%package tools
Summary:       Tools for accessing DWARF debugging information
Group:         Development/Tools
License:       GPLv2
Requires:      %{name} = %{version}-%{release}

%description
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%description static
Static libdwarf library.

%description devel
Development package containing library and header files of libdwarf.

%description tools
C++ version of dwarfdump (dwarfdump2) command-line utilities 
to access DWARF debug information.

%prep
%setup -q -n dwarf-%{version}
%patch0 -p1 -b .shlib

%build
%configure --enable-shared
LD_LIBRARY_PATH="../libdwarf" make %{?_smp_mflags} SONAME="%{soname}"

%install
install -pDm 0644 libdwarf/dwarf.h         %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pDm 0644 libdwarf/libdwarf.a      %{buildroot}%{_libdir}/libdwarf.a

install -pDm 0644 libdwarf/libdwarf.h      %{buildroot}%{_includedir}/libdwarf/libdwarf.h
install -pDm 0755 libdwarf/libdwarf.so     %{buildroot}%{_libdir}/%{sofullname}
ln      -s        %{sofullname}            %{buildroot}%{_libdir}/%{soname}
ln      -s        %{sofullname}            %{buildroot}%{_libdir}/libdwarf.so
install -pDm 0755 dwarfdump/dwarfdump      %{buildroot}%{_bindir}/dwarfdump

%post -n libdwarf -p /sbin/ldconfig

%postun -n libdwarf -p /sbin/ldconfig

%files
%doc libdwarf/ChangeLog libdwarf/README libdwarf/COPYING libdwarf/LIBDWARFCOPYRIGHT libdwarf/LGPL.txt
%{_libdir}/libdwarf.so.*

%files static
%{_libdir}/libdwarf.a

%files devel
%doc libdwarf/*.pdf
%{_includedir}/libdwarf
%{_libdir}/libdwarf.so

%files tools
%doc dwarfdump/README dwarfdump/ChangeLog dwarfdump/COPYING dwarfdump/DWARFDUMPCOPYRIGHT dwarfdump/GPL.txt
%{_bindir}/dwarfdump

%changelog
* Tue Jun 28 2016 fj <fujiang.zhu@i-soft.com.cn> - 20150915-2
- rebuilt for flatpak
