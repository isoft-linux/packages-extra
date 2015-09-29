Name:           ftgl
Version:        2.1.3
Release:        0.13.rc5%{?dist}
Summary:        OpenGL frontend to Freetype 2

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://ftgl.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ftgl/ftgl-%{version}-rc5.tar.bz2
Patch0:         ftgl-2.1.3-rc5-ttf_font.patch
Patch1:         ftgl-2.1.3-rc5-ldflags.patch

BuildRequires:  doxygen

BuildRequires:  freeglut-devel
BuildRequires:  freetype-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  cppunit-devel

Obsoletes: ftgl-utils < %{version}


%description
FTGL is a free open source library to enable developers to use arbitrary
fonts in their OpenGL (www.opengl.org)  applications.
Unlike other OpenGL font libraries FTGL uses standard font file formats
so doesn't need a preprocessing step to convert the high quality font data
into a lesser quality, proprietary format.
FTGL uses the Freetype (www.freetype.org) font library to open and 'decode'
the fonts. It then takes that output and stores it in a format most 
efficient for OpenGL rendering.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       freetype-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation

%description docs
This package contains documentation files for %{name}.


%prep
%setup -q -n ftgl-%{version}~rc5
%patch0 -p1 -b .destdir
%patch1 -p1 -b .ldflags



%build
%configure \
  --enable-shared \
  --disable-static \
  --with-gl-inc=%{_includedir} \
  --with-gl-lib=%{_libdir} \
  --with-glut-inc=%{_includedir} \
  --with-glut-lib=%{_libdir} \
  --with-x

# Remove the ~rc5 from the pc file, as this causes rpm to add a
# Requires: rpmlib(TildeInVersions) <= 4.10.0-1 
# Which breaks installing ftgl-devel into a koji buildroot (rhbz#843460)
sed -i 's/2\.1\.3~rc5/2.1.3/' ftgl.pc

make all %{?_smp_mflags}


%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Doc fixes
mkdir -p __doc/html
install -pm 0644 $RPM_BUILD_ROOT%{_datadir}/doc/ftgl/html/* __doc/html
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS BUGS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*

%files devel
%{_includedir}/FTGL/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%doc __doc/*


%changelog
