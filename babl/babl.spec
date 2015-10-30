Summary:	A dynamic, any to any, pixel format conversion library
Name:		babl
Version:	0.1.12
Release:    3	
License:	LGPLv3+ and GPLv3+
URL:		http://www.gegl.org/babl/
Source0:	ftp://ftp.gtk.org/pub/babl/0.1/%{name}-%{version}.tar.bz2
BuildRequires:	librsvg2-devel

%description
Babl is a dynamic, any to any, pixel format conversion library. It
provides conversions between the myriad of buffer types images can be
stored in. Babl doesn't only help with existing pixel formats, but also
facilitates creation of new and uncommon ones.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%prep
%setup -q

%build
%configure --disable-static --disable-introspection --disable-sse

make %{?_smp_mflags}
										
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -p'

mkdir -p babl_docs babl_docs/html
cp -pr docs/graphics docs/*.html docs/babl.css babl_docs/html
rm -rf babl_docs/html/graphics/Makefile*

rm -rf %{buildroot}%{_libdir}/*.la

# fix timestamps for multilib
touch -m --reference=docs/Makefile.am babl_docs/html{,/graphics}/*


%check
make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_libdir}/*.so.*
%{_libdir}/babl-*/

%files devel
%defattr(-, root, root, -)
%doc babl_docs/html
%{_includedir}/babl-*/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.1.12-3
- Rebuild

