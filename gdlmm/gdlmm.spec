%global apiver 3.0
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gdlmm
Version:        3.7.3
Release:        2
Summary:        C++ bindings for the gdl library

License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gdlmm/%{release_version}/gdlmm-%{version}.tar.xz

BuildRequires:  glibmm-devel
BuildRequires:  gtkmm-devel
BuildRequires:  gdl-devel

%description
This package contains C++ bindings for the GNOME Development/Docking (gdl)
library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        API documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q


%build
export CC=clang
export CXX=clang++
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

rpmclean

%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/gdlmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/gdlmm-%{apiver}/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_docdir}/gdlmm-%{apiver}/
%doc %{_datadir}/devhelp/


%changelog
