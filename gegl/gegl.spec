Summary:	A graph based image processing framework
Name:		gegl
Version:	0.2.0
Release: 	2	
License:	LGPLv3+ and GPLv3+
URL:		http://www.gegl.org/
Source0:	ftp://ftp.gtk.org/pub/gegl/0.1/%{name}-%{version}.tar.bz2
Patch0:     gegl-0.2.0-ffmpeg2-1.patch
Patch1:     gegl-0.2.0-CVE-2012-4433.patch
Patch2:     gegl-0.2.0-lua-5.2.patch
Patch3:     gegl-0.2.0-remove-src-over-op.patch

BuildRequires:	babl-devel >= 0.1.0
BuildRequires:  cairo-devel
BuildRequires:  glib2-devel >= 2.16.1
BuildRequires:  gtk2-devel >= 2.8.6
BuildRequires:  libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:  librsvg2-devel >= 2.14.0
BuildRequires:  pango-devel
BuildRequires:	perl-devel
BuildRequires:  pkgconfig
BuildRequires:  SDL-devel
BuildRequires:  exiv2-devel
BuildRequires:  lua-devel

%description
GEGL (Generic Graphics Library) is a graph based image processing framework. 
GEGLs original design was made to scratch GIMPs itches for a new
compositing and processing core. This core is being designed to have
minimal dependencies. and a simple well defined API.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig babl-devel glib2-devel

%description devel
This package contains the libraries and header files needed for
developing with %{name}.

%prep
%setup -q
chmod -x operations/external/ff-load.c operations/common/perlin/perlin.*
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export LANG=C
export CC=clang
export CXX=clang++
%configure \
    --with-exiv2 \
    --with-cairo \
    --with-gtk \
    --with-gdk-pixbuf \
    --with-libjpeg \
    --with-libpng \
    --with-librsvg \
    --without-libv4l \
    --with-pango \
    --with-pangocairo \
    --with-sdl \
    --disable-static \
    --enable-workshop \
    --disable-gtk-doc \
    --disable-introspection \
    --without-libavformat \
    --disable-docs
make %{?_smp_mflags}
										
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL='install -p'

#%check
#make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS README
%{_bindir}/gegl
%{_libdir}/*.so.*
%{_libdir}/gegl-*/

%files devel
%defattr(-, root, root, -)
%{_includedir}/gegl-*/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}*.pc
#%{_datadir}/gtk-doc/html/gegl/*
%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.0-2
- Rebuild

