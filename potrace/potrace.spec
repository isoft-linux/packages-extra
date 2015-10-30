Name:		potrace
Version:	1.12
Release:	3%{?dist}
Summary:	Transform bitmaps into vector graphics
# README defines license as GPLv2+
License:	GPLv2+
URL:		http://potrace.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Documentation
Source1:	http://potrace.sourceforge.net/potrace.pdf
Source2:	http://potrace.sourceforge.net/potracelib.pdf
# Patch for supporting 64 bit ARM from upstream
Patch0:		potrace-1.11-autoconf.diff

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	zlib-devel

%description
Potrace is a utility for tracing a bitmap, which means, transforming a bitmap 
into a smooth, scalable image. The input is a bitmap (PBM, PGM, PPM, or BMP
format), and the default output is an encapsulated PostScript file (EPS).
A typical use is to create EPS files from scanned data, such as company or
university logos, handwritten notes, etc. The resulting image is not "jaggy"
like a bitmap, but smooth. It can then be rendered at any resolution.

Potrace can currently produce the following output formats: EPS, PostScript,
PDF, SVG (scalable vector graphics), Xfig, Gimppath, and PGM (for easy
antialiasing). Additional backends might be added in the future.

Mkbitmap is a program distributed with Potrace which can be used to pre-process
the input for better tracing behavior on greyscale and color images.


%package devel
Summary:	Potrace development library and headers
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the potrace development library and headers.


%package doc
Summary:	Documentation on how to use the potrace library
BuildArch:	noarch

%description doc
This package contains documentation for the potrace algorithm and the potrace
library.

%prep
%setup -q
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .

%build
%configure --enable-shared --disable-static \
 --enable-metric --with-libpotrace --with-pic
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name *.la -exec rm -rf {} \;

# Get rid of installed copy of placement.pdf
rm -rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc/placement.pdf
%{_bindir}/potrace
%{_bindir}/mkbitmap
%{_libdir}/libpotrace.so.*
%{_mandir}/man1/potrace.1.*
%{_mandir}/man1/mkbitmap.1.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libpotrace.so
%{_includedir}/potracelib.h

%files doc
%defattr(-,root,root,-)
%doc potrace.pdf potracelib.pdf

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.12-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
