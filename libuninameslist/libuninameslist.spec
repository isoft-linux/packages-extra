Name:           libuninameslist
Version:        20130501
Release:        4%{?dist}

Summary:        A library providing Unicode character names and annotations

Group:          System Environment/Libraries
License:        BSD
URL:            http://libuninameslist.sourceforge.net
Source0:        https://github.com/fontforge/libuninameslist/archive/Version_0.3.20130501.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
libuninameslist provides applications with access to Unicode name and
annotation data from the official Unicode Character Database.

%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q -n libuninameslist-Version_0.3.20130501

%build
autoreconf -i
automake --foreign -Wall
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall incdir=$RPM_BUILD_ROOT%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*


%changelog
