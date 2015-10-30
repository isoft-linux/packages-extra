%filter_provides_in %{_libdir}/GraphicsMagick-%{version}
%filter_setup

Summary: An ImageMagick fork, offering faster image generation and better quality
Name: GraphicsMagick
Version: 1.3.22
Release: 2%{?dist}

License: MIT
Source0: http://downloads.sourceforge.net/sourceforge/graphicsmagick/GraphicsMagick-%{version}.tar.xz
Url: http://www.graphicsmagick.org/

## upstreamable patches
Patch50: GraphicsMagick-1.3.14-perl_linkage.patch

## upstream patches

BuildRequires: bzip2-devel
BuildRequires: cups-client
BuildRequires: freetype-devel
BuildRequires: jasper-devel
BuildRequires: jbigkit-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libtiff-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libungif-devel
BuildRequires: libwebp-devel
BuildRequires: libwmf-devel
BuildRequires: libxml2-devel
BuildRequires: libX11-devel libXext-devel libXt-devel
BuildRequires: p7zip
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: xdg-utils
BuildRequires: xz-devel
BuildRequires: zlib-devel
## FIXME: %%check stuff
#BuildRequires: xorg-x11-server-Xvfb

# depend on stuff referenced below
# --with-gs-font-dir=%{_datadir}/fonts/default/Type1
Requires: urw-fonts

%description
GraphicsMagick is a comprehensive image processing package which is initially
based on ImageMagick 5.5.2, but which has undergone significant re-work by
the GraphicsMagick Group to significantly improve the quality and performance
of the software.

%package devel
Summary: Libraries and header files for GraphicsMagick app development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications. GraphicsMagick is an image
manipulation program.

If you want to create applications that will use GraphicsMagick code or
APIs, you need to install GraphicsMagick-devel as well as GraphicsMagick.
You do not need to install it if you just want to use GraphicsMagick,
however.

%package doc
Summary: GraphicsMagick documentation
# upgrade path for introduction of -doc subpkg in 1.3.19-4
Obsoletes: GraphicsMagick < 1.3.19-4
%{!?el5:BuildArch: noarch}

%description doc
Documentation for GraphicsMagick.

%package perl
Summary: GraphicsMagick perl bindings
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to GraphicsMagick.

Install GraphicsMagick-perl if you want to use any perl scripts that use
GraphicsMagick.

%package c++
Summary: GraphicsMagick Magick++ library (C++ bindings)
Requires: %{name}%{?_isa} = %{version}-%{release}

%description c++
This package contains the GraphicsMagick++ library, a C++ binding to the 
GraphicsMagick graphics manipulation library.

Install GraphicsMagick-c++ if you want to use any applications that use 
GraphicsMagick++.

%package c++-devel
Summary: C++ bindings for the GraphicsMagick library
Requires: %{name}-c++%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description c++-devel
GraphicsMagick-devel contains the Libraries and header files you'll
need to develop GraphicsMagick applications using the Magick++ C++ bindings.
GraphicsMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install GraphicsMagick-c++-devel, ImageMagick-devel and
GraphicsMagick.
You don't need to install it if you just want to use GraphicsMagick, or if you
want to develop/compile applications using the GraphicsMagick C interface,
however.

%prep
%setup -q
%patch50 -p1 -b .perl_linkage

for f in ChangeLog.{2006,2008,2009,2012} NEWS.txt ; do
    iconv -f iso-8859-2 -t utf8 < $f > $f.utf8
    touch -r $f $f.utf8 ; mv -f $f.utf8 $f
done

# Avoid lib64 rpaths (FIXME: recheck this on newer releases)
%if "%{_libdir}" != "/usr/lib"
sed -i.rpath -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure --enable-shared --disable-static \
           --docdir=%{_pkgdocdir} \
           --with-lcms2 \
           --with-magick_plus_plus \
           --with-modules \
           --with-perl \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix}" \
           --with-quantum-depth=16 \
           --enable-quantum-library-names \
           --with-threads \
           --with-wmf \
           --with-x \
           --with-xml \
           --without-dps \
           --without-gslib \
           --with-gs-font-dir=%{_datadir}/fonts/default/Type1

make %{?_smp_mflags}
make %{?_smp_mflags} perl-build


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot} -C PerlMagick

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

find %{buildroot} -name "*.bs" |xargs rm -fv
find %{buildroot} -name ".packlist" |xargs rm -fv
find %{buildroot} -name "perllocal.pod" |xargs rm -fv

chmod 755 %{buildroot}%{perl_vendorarch}/auto/Graphics/Magick/Magick.so

# perlmagick: build files list
find %{buildroot}/%{_libdir}/perl* -type f -print \
    | sed "s@^%{buildroot}@@g" > perl-pkg-files 
find %{buildroot}%{perl_vendorarch} -type d -print \
    | sed "s@^%{buildroot}@%dir @g" \
    | grep -v '^%dir %{perl_vendorarch}$' \
    | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

rm -rf %{buildroot}%{_datadir}/GraphicsMagick
# Keep config
rm -rf %{buildroot}%{_datadir}/%{name}-%{version}/[a-b,d-z,A-Z]*
rm -vf  %{buildroot}%{_libdir}/lib*.la

## unpackaged files
rm -f %{buildroot}%{_pkgdocdir}/Copyright.txt

%check
#make %{?_smp_mflags} check ||:

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%global libQ -Q16

%files
%license Copyright.txt
%{_libdir}/libGraphicsMagick%{?libQ}.so.3*
%{_libdir}/libGraphicsMagickWand%{?libQ}.so.2*
%{_bindir}/[a-z]*
%{_libdir}/GraphicsMagick-%{version}/
%{_datadir}/GraphicsMagick-%{version}/
%{_mandir}/man[145]/[a-z]*

%files devel
%{_bindir}/GraphicsMagick-config
%{_bindir}/GraphicsMagickWand-config
%{_libdir}/libGraphicsMagick.so
%{_libdir}/libGraphicsMagickWand.so
%{_libdir}/pkgconfig/GraphicsMagick.pc
%{_libdir}/pkgconfig/GraphicsMagickWand.pc
%dir %{_includedir}/GraphicsMagick/
%{_includedir}/GraphicsMagick/magick/
%{_includedir}/GraphicsMagick/wand/
%{_mandir}/man1/GraphicsMagick-config.*
%{_mandir}/man1/GraphicsMagickWand-config.*

%files doc
%{_pkgdocdir}

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files c++
%{_libdir}/libGraphicsMagick++%{?libQ}.so.12*

%files c++-devel
%{_bindir}/GraphicsMagick++-config
%{_includedir}/GraphicsMagick/Magick++/
%{_includedir}/GraphicsMagick/Magick++.h
%{_libdir}/libGraphicsMagick++.so
%{_libdir}/pkgconfig/GraphicsMagick++.pc
%{_mandir}/man1/GraphicsMagick++-config.*

%files perl -f perl-pkg-files
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.3.22-2
- Rebuild

