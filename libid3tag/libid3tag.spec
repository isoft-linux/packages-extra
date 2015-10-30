Name:           libid3tag
Version:        0.15.1b
Release:        22%{?dist}
Summary:        ID3 tag manipulation library
License:        GPLv2+
URL:            http://www.underbit.com/products/mad/
Source0:        http://downloads.sourceforge.net/mad/%{name}-%{version}.tar.gz
Patch0:         libid3tag-0.15.1b-fix_overflow.patch
BuildRequires:  zlib-devel >= 1.1.4

%description
libid3tag is a library for reading and (eventually) writing ID3 tags,
both ID3v1 and the various versions of ID3v2.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
ID3 tag library development files.


%prep
%setup -q
%patch0 -p0 -b .CVE-2008-2109

# *.pc originally from the Debian package.
cat << \EOF > %{name}.pc
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: id3tag
Description: ID3 tag manipulation library
Requires:
Version: %{version}
Libs: -lid3tag
Cflags:
EOF


%build
%configure --disable-static
# configure strips -g, -O2 from CFLAGS, override it here
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
install -Dpm 644 %{name}.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/id3tag.pc


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_libdir}/libid3tag.so.*

%files devel
%{_includedir}/id3tag.h
%{_libdir}/libid3tag.so
%{_libdir}/pkgconfig/id3tag.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.15.1b-22
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.15.1b-21
- Initial build

