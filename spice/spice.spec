Summary:SPICE: Simple Protocol for Independent Computing Environments
Name: spice
Version: 0.12.5
Release: 1
License: LGPLv2+
Group: User Interface/Desktops 
Source: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: spice-protocol, celt051-devel, libcacard-devel, pyparsing
%description
SPICE is a remote display system built for virtual environments which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.

%package -n libspice
Summary:        Runtime libraries for %{name}
Group:          System Environment/Libraries

%description -n libspice
This package contains runtime library of %{name}


%package -n libspice-devel
Summary:        Development libraries and header files for %{name}
Group:          Development/Libraries
Requires:       libspice = %{version}-%{release}

%description -n libspice-devel
This package contains Development libraries and header files of %{name}

%prep
%setup -q

%build
export CC=clang
export CXX=clang++
%configure --disable-client --without-sasl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

#%files
#%defattr(-, root, root, -)
#%{_bindir}/spicec

%files -n libspice
%{_libdir}/*.so.*

%files -n libspice-devel
%defattr(-, root, root, -)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/spice-server
%{_libdir}/pkgconfig/*.pc
