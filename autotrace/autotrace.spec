Name:           autotrace
Version:        0.31.1
Release:        42
Summary:        Utility for converting bitmaps to vector graphics
License:        GPLv2+ and LGPLv2+
URL:            http://autotrace.sourceforge.net/
Source0:        http://download.sf.net/autotrace/autotrace-0.31.1.tar.gz
Patch1:         autotrace-0001-Modify-GetOnePixel-usage-to-build-against-current-Im.patch
Patch2:         autotrace-0002-Fixed-underquoted-AM_PATH_AUTOTRACE-definition.patch
Patch3:         autotrace-0003-libpng-fix.patch
# Sent upstream
Patch4:         autotrace-0.31.1-CVE-2013-1953.patch
Patch5:         autotrace-0.31.1-multilib-fix.patch
BuildRequires:  ImageMagick-devel
BuildRequires:  libpng-devel > 2:1.2
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  bzip2-devel
BuildRequires:  freetype-devel
# For autoreconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool


%description
AutoTrace is a program for converting bitmaps to vector graphics.

Supported input formats include BMP, TGA, PNM, PPM, and any format
supported by ImageMagick, whereas output can be produced in
Postscript, SVG, xfig, SWF, and others.

%package devel
Summary:        Header files for autotrace
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ImageMagick-devel


%description devel
This package contains header files and development libraries for autotrace.


%prep
%setup -q
%patch1 -p1 -b .GetOnePixel
%patch2 -p1 -b .aclocal18
%patch3 -p1 -b .libpng15
%patch4 -p1 -b .CVE-2013-1953
%patch5 -p1 -b .multilib-fix

%build
autoreconf -ivf 
%configure

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_bindir}/autotrace
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%{_bindir}/autotrace-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/autotrace.pc
%{_includedir}/autotrace/
%{_datadir}/aclocal/autotrace.m4


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.31.1-42
- Rebuild

