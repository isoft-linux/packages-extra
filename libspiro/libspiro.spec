Name:           libspiro
Version:        20150131
Release:        2%{?dist}
Summary:        Library to simplify the drawing of beautiful curves

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libspiro.sourceforge.net/
Source0:        https://github.com/fontforge/libspiro/archive/0.3.20150131.tar.gz
BuildRequires: automake autoconf libtool

%description
This library will take an array of spiro control points and 
convert them into a series of bézier splines which can then 
be used in the myriad of ways the world has come to use béziers. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n libspiro-0.3.20150131

%build
autoreconf -i
automake --foreign -Wall
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README* ChangeLog AUTHORS
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libspiro.pc

%changelog
