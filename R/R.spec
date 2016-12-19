%define _jvmdir /usr/lib/jvm/openjdk8

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name: R
Version: 3.2.1
Release: 5%{?dist}
Summary: A language for data analysis and graphics
URL: http://www.r-project.org
Source0: ftp://cran.r-project.org/pub/R/src/base/R-3/R-%{version}.tar.gz
Source1: macros.R
Source2: R-make-search-index.sh
Patch0: R-fix-with-texinfo-6.0.patch

License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-gfortran
BuildRequires: gcc
BuildRequires: libpng-devel, libjpeg-devel, readline-devel
BuildRequires: tcl-devel, tk-devel, ncurses-devel
BuildRequires: pcre-devel, zlib-devel
BuildRequires: libcurl-devel
BuildRequires: texinfo
BuildRequires: tre-devel

# valgrind is available only on selected arches
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64
BuildRequires: valgrind-devel
%endif

BuildRequires: openjdk

BuildRequires: lapack-devel >= 3.5.0-7
BuildRequires: blas-devel >= 3.5.0-7

BuildRequires: libSM-devel, libX11-devel, libICE-devel, libXt-devel
BuildRequires: bzip2-devel, libXmu-devel, cairo-devel, libtiff-devel
BuildRequires: pango-devel, xz-devel
BuildRequires: libicu-devel

BuildRequires: less
# R-devel will pull in R-core
Requires: R-devel = %{version}-%{release}
# libRmath-devel will pull in libRmath
Requires: libRmath-devel = %{version}-%{release}
# Pull in Java bits (if you don't want this, use R-core)
Requires: R-java = %{version}-%{release}

%description
This is a metapackage that provides both core R userspace and 
all R development components.

R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core
Summary: The minimal R components necessary for a functional runtime
Requires: xdg-utils, cups
Requires: vim
Requires: perl, sed, gawk, less, make, unzip

# These are the submodules that R-core provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are provided for 
# packager convenience.
Provides: R-base = %{version}
Provides: R-boot = 1.3.16
Provides: R-class = 7.3.12
Provides: R-cluster = 2.0.1
Provides: R-codetools = 0.2.11
Provides: R-datasets = %{version}
Provides: R-foreign = 0.8.63
Provides: R-graphics = %{version}
Provides: R-grDevices = %{version}
Provides: R-grid = %{version}
Provides: R-KernSmooth = 2.23.14
Provides: R-lattice = 0.20.31
Provides: R-MASS = 7.3.40
Provides: R-Matrix = 1.2.1
Obsoletes: R-Matrix < 0.999375-7
Provides: R-methods = %{version}
Provides: R-mgcv = 1.8.6
Provides: R-nlme = 3.1.120
Provides: R-nnet = 7.3.9
Provides: R-parallel = %{version}
Provides: R-rpart = 4.1.9
Provides: R-spatial = 7.3.9
Provides: R-splines = %{version}
Provides: R-stats = %{version}
Provides: R-stats4 = %{version}
Provides: R-survival = 2.38.1
Provides: R-tcltk = %{version}
Provides: R-tools = %{version}
Provides: R-utils = %{version}

%description core
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core-devel
Summary: Core files for development of R packages (no Java)
Requires: R-core = %{version}-%{release}
# You need all the BuildRequires for the development version
Requires: gcc, gcc-gfortran
Requires: bzip2-devel, libX11-devel, pcre-devel, zlib-devel
Requires: tcl-devel, tk-devel, pkgconfig, xz-devel
Requires: blas-devel >= 3.0, lapack-devel
Requires: libicu-devel
Requires: qpdf
Requires: tre-devel


Provides: R-Matrix-devel = 1.2.1
Obsoletes: R-Matrix-devel < 0.999375-7

%description core-devel
Install R-core-devel if you are going to develop or compile R packages.
This package does not configure the R environment for Java, install
R-java-devel if you want this.

%package devel
Summary: Full R development environment metapackage
Requires: R-core-devel = %{version}-%{release}
Requires: R-java-devel = %{version}-%{release}

%description devel
This is a metapackage to install a complete (with Java) R development
environment.

%package java
Summary: R with Fedora provided Java Runtime Environment
Requires(post): R-core = %{version}-%{release}
Requires(post): openjdk 

%description java
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

This package also has an additional dependency on java, as provided by
Fedora's openJDK.

%package java-devel
Summary: Development package for use with Java enabled R components
Requires(post): R-core-devel = %{version}-%{release}
Requires(post): openjdk

%description java-devel
Install R-java-devel if you are going to develop or compile R packages
that assume java is present and configured on the system.

%package -n libRmath
Summary: Standalone math library from the R project

%description -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the shared libRmath library.

%package -n libRmath-devel
Summary: Headers from the R Standalone math library
Requires: libRmath = %{version}-%{release}, pkgconfig

%description -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the libRmath header files.

%package -n libRmath-static
Summary: Static R Standalone math library
Requires: libRmath-devel = %{version}-%{release}

%description -n libRmath-static
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the static libRmath library.

%prep
%setup -q
%patch0 -p1

# Filter false positive provides.
cat <<EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} \
| grep -v 'File::Copy::Recursive' | grep -v 'Text::DelimMatch'
EOF
%define __perl_provides %{_builddir}/R-%{version}/%{name}-prov
chmod +x %{__perl_provides}

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} \
| grep -v 'perl(Text::DelimMatch)'
EOF
%define __perl_requires %{_builddir}/R-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
# Add PATHS to Renviron for R_LIBS_SITE
echo 'R_LIBS_SITE=${R_LIBS_SITE-'"'/usr/local/lib/R/site-library:/usr/local/lib/R/library:%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

case "%{_target_cpu}" in
      x86_64|mips64|ppc64|powerpc64|sparc64|s390x|powerpc64le|ppc64le)
          export CC="gcc -m64"
          export CXX="g++ -m64"
          export F77="gfortran -m64"
          export FC="gfortran -m64"
      ;;
      ia64|alpha|arm*|aarch64|sh*)
          export CC="gcc"
          export CXX="g++"
          export F77="gfortran"
          export FC="gfortran"
      ;;
      s390)
          export CC="gcc -m31"
          export CXX="g++ -m31"
          export F77="gfortran -m31"
          export FC="gfortran -m31"
      ;;    
      *)
          export CC="gcc -m32"
          export CXX="g++ -m32"
          export F77="gfortran -m32"
          export FC="gfortran -m32"
      ;;    
esac

export CFLAGS="%{optflags} -ffat-lto-objects"
export CXXFLAGS="%{optflags} -ffat-lto-objects"
export FCFLAGS="%{optflags} -ffat-lto-objects"

( %configure \
    --with-system-tre \
    --with-system-zlib \
    --with-system-bzlib \
    --with-system-pcre \
    --with-system-valgrind-headers \
    --with-lapack \
    --with-blas \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib \
    --enable-prebuilt-html \
%ifnarch %{arm}
    --enable-lto \
%endif
    rdocdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} \
    rincludedir=%{_includedir}/R \
    rsharedir=%{_datadir}/R) \
 > CONFIGURE.log
cat CONFIGURE.log | grep -A30 'R is now' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
# What a hack.
# Current texinfo doesn't like @eqn. Use @math instead where stuff breaks.
cp doc/manual/R-exts.texi doc/manual/R-exts.texi.spot
cp doc/manual/R-intro.texi doc/manual/R-intro.texi.spot
sed -i 's|@eqn|@math|g' doc/manual/R-exts.texi
sed -i 's|@eqn|@math|g' doc/manual/R-intro.texi

make info

# Convert to UTF-8
for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1; do
  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
  mv $i{.utf8,}
done

%install
make DESTDIR=${RPM_BUILD_ROOT} install install-info
# And now, undo the hack. :P
mv doc/manual/R-exts.texi.spot doc/manual/R-exts.texi
mv doc/manual/R-intro.texi.spot doc/manual/R-intro.texi

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old
mkdir -p ${RPM_BUILD_ROOT}%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
install -p CAPABILITIES ${RPM_BUILD_ROOT}%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

#Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=${RPM_BUILD_ROOT})

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library

# Install rpm helper macros
mkdir -p $RPM_BUILD_ROOT%{macrosdir}/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{macrosdir}/

# Install rpm helper script
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm/
install -m0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/rpm/

# Fix multilib
touch -r README ${RPM_BUILD_ROOT}%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}/CAPABILITIES
touch -r README doc/manual/*.pdf
touch -r README $RPM_BUILD_ROOT%{_bindir}/R

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
sed -i 's|\..\/\..|%{_libdir}/R|g' $RPM_BUILD_ROOT%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}/html/packages.html

for i in $RPM_BUILD_ROOT%{_libdir}/R/library/*/html/*.html; do
  sed -i 's|\..\/\..\/..\/doc|%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}|g' $i
done

# Fix exec bits
chmod +x $RPM_BUILD_ROOT%{_datadir}/R/sh/echo.sh
chmod -x $RPM_BUILD_ROOT%{_libdir}/R/library/mgcv/CITATION ${RPM_BUILD_ROOT}%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}/CAPABILITIES

# Symbolic link for convenience
pushd $RPM_BUILD_ROOT%{_libdir}/R
ln -s ../../include/R include
popd

# Symbolic link for LaTeX
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex
pushd $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex
ln -s ../../../R/texmf/tex/latex R
popd

%check
# Needed by tests/ok-error.R, which will smash the stack on PPC64. This is the purpose of the test.
ulimit -s 16384
make check

%files
# Metapackage

%files core
%defattr(-, root, root, -)
%{_bindir}/R
%{_bindir}/Rscript
%{_datadir}/R/
%{_datadir}/texmf/
# Have to break this out for the translations
%dir %{_libdir}/R/
%{_libdir}/R/bin/
%dir %{_libdir}/R/etc
%config %{_libdir}/R/etc/Makeconf
%config(noreplace) %{_libdir}/R/etc/Renviron
%config(noreplace) %{_libdir}/R/etc/javaconf
%config(noreplace) %{_libdir}/R/etc/ldpaths
%config(noreplace) %{_libdir}/R/etc/repositories
%{_libdir}/R/lib/
%dir %{_libdir}/R/library/
%dir %{_libdir}/R/library/translations/
%{_libdir}/R/library/translations/DESCRIPTION
%lang(da) %{_libdir}/R/library/translations/da/
%lang(de) %{_libdir}/R/library/translations/de/
%lang(en) %{_libdir}/R/library/translations/en*/
%lang(es) %{_libdir}/R/library/translations/es/
%lang(fa) %{_libdir}/R/library/translations/fa/
%lang(fr) %{_libdir}/R/library/translations/fr/
%lang(it) %{_libdir}/R/library/translations/it/
%lang(ja) %{_libdir}/R/library/translations/ja/
%lang(ko) %{_libdir}/R/library/translations/ko/
%lang(nn) %{_libdir}/R/library/translations/nn/
%lang(pl) %{_libdir}/R/library/translations/pl/
%lang(pt) %{_libdir}/R/library/translations/pt*/
%lang(ru) %{_libdir}/R/library/translations/ru/
%lang(tr) %{_libdir}/R/library/translations/tr/
%lang(zh) %{_libdir}/R/library/translations/zh*/
# base
%{_libdir}/R/library/base/
# boot
%dir %{_libdir}/R/library/boot/
%{_libdir}/R/library/boot/bd.q
%{_libdir}/R/library/boot/CITATION
%{_libdir}/R/library/boot/data/
%{_libdir}/R/library/boot/DESCRIPTION
%{_libdir}/R/library/boot/help/
%{_libdir}/R/library/boot/html/
%{_libdir}/R/library/boot/INDEX
%{_libdir}/R/library/boot/Meta/
%{_libdir}/R/library/boot/NAMESPACE
%dir %{_libdir}/R/library/boot/po/
%lang(de) %{_libdir}/R/library/boot/po/de/
%lang(en) %{_libdir}/R/library/boot/po/en*/
%lang(fr) %{_libdir}/R/library/boot/po/fr/
%lang(ko) %{_libdir}/R/library/boot/po/ko/
%lang(pl) %{_libdir}/R/library/boot/po/pl/
%lang(ru) %{_libdir}/R/library/boot/po/ru/
%{_libdir}/R/library/boot/R/
# class
%dir %{_libdir}/R/library/class/
%{_libdir}/R/library/class/CITATION
%{_libdir}/R/library/class/DESCRIPTION
%{_libdir}/R/library/class/help/
%{_libdir}/R/library/class/html/
%{_libdir}/R/library/class/INDEX
%{_libdir}/R/library/class/libs/
%{_libdir}/R/library/class/Meta/
%{_libdir}/R/library/class/NAMESPACE
%{_libdir}/R/library/class/NEWS
%dir %{_libdir}/R/library/class/po/
%lang(de) %{_libdir}/R/library/class/po/de/
%lang(en) %{_libdir}/R/library/class/po/en*/
%lang(fr) %{_libdir}/R/library/class/po/fr/
%lang(ko) %{_libdir}/R/library/class/po/ko/
%lang(pl) %{_libdir}/R/library/class/po/pl/
%{_libdir}/R/library/class/R/
# cluster
%dir %{_libdir}/R/library/cluster/
%{_libdir}/R/library/cluster/CITATION
%{_libdir}/R/library/cluster/data/
%{_libdir}/R/library/cluster/DESCRIPTION
%{_libdir}/R/library/cluster/help/
%{_libdir}/R/library/cluster/html/
%{_libdir}/R/library/cluster/INDEX
%{_libdir}/R/library/cluster/libs/
%{_libdir}/R/library/cluster/Meta/
%{_libdir}/R/library/cluster/NAMESPACE
%{_libdir}/R/library/cluster/R/
%dir %{_libdir}/R/library/cluster/po/
%lang(de) %{_libdir}/R/library/cluster/po/de/
%lang(en) %{_libdir}/R/library/cluster/po/en*/
%lang(fr) %{_libdir}/R/library/cluster/po/fr/
%lang(pl) %{_libdir}/R/library/cluster/po/pl/
# codetools
%dir %{_libdir}/R/library/codetools/
%{_libdir}/R/library/codetools/DESCRIPTION
%{_libdir}/R/library/codetools/help/
%{_libdir}/R/library/codetools/html/
%{_libdir}/R/library/codetools/INDEX
%{_libdir}/R/library/codetools/Meta/
%{_libdir}/R/library/codetools/NAMESPACE
%{_libdir}/R/library/codetools/R/
# compiler
%{_libdir}/R/library/compiler/
# datasets
%{_libdir}/R/library/datasets/
# foreign
%dir %{_libdir}/R/library/foreign/
%{_libdir}/R/library/foreign/COPYRIGHTS
%{_libdir}/R/library/foreign/DESCRIPTION
%{_libdir}/R/library/foreign/files/
%{_libdir}/R/library/foreign/help/
%{_libdir}/R/library/foreign/html/
%{_libdir}/R/library/foreign/INDEX
%{_libdir}/R/library/foreign/libs/
%{_libdir}/R/library/foreign/Meta/
%{_libdir}/R/library/foreign/NAMESPACE
%dir %{_libdir}/R/library/foreign/po/
%lang(de) %{_libdir}/R/library/foreign/po/de/
%lang(en) %{_libdir}/R/library/foreign/po/en*/
%lang(fr) %{_libdir}/R/library/foreign/po/fr/
%lang(pl) %{_libdir}/R/library/foreign/po/pl/
%{_libdir}/R/library/foreign/R/
# graphics
%{_libdir}/R/library/graphics/
# grDevices
%{_libdir}/R/library/grDevices
# grid
%{_libdir}/R/library/grid/
# KernSmooth
%dir %{_libdir}/R/library/KernSmooth/
%{_libdir}/R/library/KernSmooth/DESCRIPTION
%{_libdir}/R/library/KernSmooth/help/
%{_libdir}/R/library/KernSmooth/html/
%{_libdir}/R/library/KernSmooth/INDEX
%{_libdir}/R/library/KernSmooth/libs/
%{_libdir}/R/library/KernSmooth/Meta/
%{_libdir}/R/library/KernSmooth/NAMESPACE
%dir %{_libdir}/R/library/KernSmooth/po/
%lang(de) %{_libdir}/R/library/KernSmooth/po/de/
%lang(en) %{_libdir}/R/library/KernSmooth/po/en*/
%lang(fr) %{_libdir}/R/library/KernSmooth/po/fr/
%lang(ko) %{_libdir}/R/library/KernSmooth/po/ko/
%lang(pl) %{_libdir}/R/library/KernSmooth/po/pl/
%{_libdir}/R/library/KernSmooth/R/
# lattice
%dir %{_libdir}/R/library/lattice/
%{_libdir}/R/library/lattice/CITATION
%{_libdir}/R/library/lattice/data/
%{_libdir}/R/library/lattice/demo/
%{_libdir}/R/library/lattice/DESCRIPTION
%{_libdir}/R/library/lattice/help/
%{_libdir}/R/library/lattice/html/
%{_libdir}/R/library/lattice/INDEX
%{_libdir}/R/library/lattice/libs/
%{_libdir}/R/library/lattice/Meta/
%{_libdir}/R/library/lattice/NAMESPACE
%{_libdir}/R/library/lattice/NEWS
%dir %{_libdir}/R/library/lattice/po/
%lang(de) %{_libdir}/R/library/lattice/po/de/
%lang(en) %{_libdir}/R/library/lattice/po/en*/
%lang(fr) %{_libdir}/R/library/lattice/po/fr/
%lang(ko) %{_libdir}/R/library/lattice/po/ko/
%lang(pl) %{_libdir}/R/library/lattice/po/pl*/
%{_libdir}/R/library/lattice/R/
# MASS
%dir %{_libdir}/R/library/MASS/
%{_libdir}/R/library/MASS/CITATION
%{_libdir}/R/library/MASS/data/
%{_libdir}/R/library/MASS/DESCRIPTION
%{_libdir}/R/library/MASS/help/
%{_libdir}/R/library/MASS/html/
%{_libdir}/R/library/MASS/INDEX
%{_libdir}/R/library/MASS/libs/
%{_libdir}/R/library/MASS/Meta/
%{_libdir}/R/library/MASS/NAMESPACE
%{_libdir}/R/library/MASS/NEWS
%dir %{_libdir}/R/library/MASS/po
%lang(de) %{_libdir}/R/library/MASS/po/de/
%lang(en) %{_libdir}/R/library/MASS/po/en*/
%lang(fr) %{_libdir}/R/library/MASS/po/fr/
%lang(ko) %{_libdir}/R/library/MASS/po/ko/
%lang(pl) %{_libdir}/R/library/MASS/po/pl/
%{_libdir}/R/library/MASS/R/
%{_libdir}/R/library/MASS/scripts/
# Matrix
%dir %{_libdir}/R/library/Matrix/
%{_libdir}/R/library/Matrix/Copyrights
%{_libdir}/R/library/Matrix/data/
%{_libdir}/R/library/Matrix/doc/
%{_libdir}/R/library/Matrix/DESCRIPTION
%{_libdir}/R/library/Matrix/Doxyfile
%{_libdir}/R/library/Matrix/external/
%{_libdir}/R/library/Matrix/help/
%{_libdir}/R/library/Matrix/html/
%{_libdir}/R/library/Matrix/include/
%{_libdir}/R/library/Matrix/INDEX
%{_libdir}/R/library/Matrix/libs/
%{_libdir}/R/library/Matrix/Meta/
%{_libdir}/R/library/Matrix/NAMESPACE
%{_libdir}/R/library/Matrix/NEWS.Rd
%dir %{_libdir}/R/library/Matrix/po/
%lang(de) %{_libdir}/R/library/Matrix/po/de/
%lang(en) %{_libdir}/R/library/Matrix/po/en*/
%lang(fr) %{_libdir}/R/library/Matrix/po/fr/
%lang(ko) %{_libdir}/R/library/Matrix/po/ko/
%lang(pl) %{_libdir}/R/library/Matrix/po/pl/
%{_libdir}/R/library/Matrix/R/
%{_libdir}/R/library/Matrix/test-tools.R
%{_libdir}/R/library/Matrix/test-tools-1.R
%{_libdir}/R/library/Matrix/test-tools-Matrix.R
# methods
%{_libdir}/R/library/methods/
# mgcv
%{_libdir}/R/library/mgcv/
# nlme
%dir %{_libdir}/R/library/nlme/
%{_libdir}/R/library/nlme/CITATION
%{_libdir}/R/library/nlme/data/
%{_libdir}/R/library/nlme/DESCRIPTION
%{_libdir}/R/library/nlme/help/
%{_libdir}/R/library/nlme/html/
%{_libdir}/R/library/nlme/INDEX
%{_libdir}/R/library/nlme/libs/
%{_libdir}/R/library/nlme/Meta/
%{_libdir}/R/library/nlme/mlbook/
%{_libdir}/R/library/nlme/NAMESPACE
%dir %{_libdir}/R/library/nlme/po/
%lang(de) %{_libdir}/R/library/nlme/po/de/
%lang(en) %{_libdir}/R/library/nlme/po/en*/
%lang(fr) %{_libdir}/R/library/nlme/po/fr/
%lang(ko) %{_libdir}/R/library/nlme/po/ko/
%lang(pl) %{_libdir}/R/library/nlme/po/pl/
%{_libdir}/R/library/nlme/R/
%{_libdir}/R/library/nlme/scripts/
# nnet
%dir %{_libdir}/R/library/nnet/
%{_libdir}/R/library/nnet/CITATION
%{_libdir}/R/library/nnet/DESCRIPTION
%{_libdir}/R/library/nnet/help/
%{_libdir}/R/library/nnet/html/
%{_libdir}/R/library/nnet/INDEX
%{_libdir}/R/library/nnet/libs/
%{_libdir}/R/library/nnet/Meta/
%{_libdir}/R/library/nnet/NAMESPACE
%{_libdir}/R/library/nnet/NEWS
%dir %{_libdir}/R/library/nnet/po
%lang(de) %{_libdir}/R/library/nnet/po/de/
%lang(en) %{_libdir}/R/library/nnet/po/en*/
%lang(fr) %{_libdir}/R/library/nnet/po/fr/
%lang(ko) %{_libdir}/R/library/nnet/po/ko/
%lang(pl) %{_libdir}/R/library/nnet/po/pl/
%{_libdir}/R/library/nnet/R/
# parallel
%{_libdir}/R/library/parallel/
# rpart
%dir %{_libdir}/R/library/rpart/
%{_libdir}/R/library/rpart/data/
%{_libdir}/R/library/rpart/DESCRIPTION
%{_libdir}/R/library/rpart/doc/
%{_libdir}/R/library/rpart/help/
%{_libdir}/R/library/rpart/html/
%{_libdir}/R/library/rpart/INDEX
%{_libdir}/R/library/rpart/libs/
%{_libdir}/R/library/rpart/Meta/
%{_libdir}/R/library/rpart/NAMESPACE
%{_libdir}/R/library/rpart/NEWS.Rd
%dir %{_libdir}/R/library/rpart/po
%lang(de) %{_libdir}/R/library/rpart/po/de/
%lang(en) %{_libdir}/R/library/rpart/po/en*/
%lang(fr) %{_libdir}/R/library/rpart/po/fr/
%lang(ko) %{_libdir}/R/library/rpart/po/ko/
%lang(pl) %{_libdir}/R/library/rpart/po/pl/
%lang(ru) %{_libdir}/R/library/rpart/po/ru/
%{_libdir}/R/library/rpart/R/
# spatial
%dir %{_libdir}/R/library/spatial/
%{_libdir}/R/library/spatial/CITATION
%{_libdir}/R/library/spatial/DESCRIPTION
%{_libdir}/R/library/spatial/help/
%{_libdir}/R/library/spatial/html/
%{_libdir}/R/library/spatial/INDEX
%{_libdir}/R/library/spatial/libs/
%{_libdir}/R/library/spatial/Meta/
%{_libdir}/R/library/spatial/NAMESPACE
%{_libdir}/R/library/spatial/NEWS
%dir %{_libdir}/R/library/spatial/po
%lang(de) %{_libdir}/R/library/spatial/po/de/
%lang(en) %{_libdir}/R/library/spatial/po/en*/
%lang(fr) %{_libdir}/R/library/spatial/po/fr/
%lang(ko) %{_libdir}/R/library/spatial/po/ko/
%lang(pl) %{_libdir}/R/library/spatial/po/pl/
%{_libdir}/R/library/spatial/ppdata/
%{_libdir}/R/library/spatial/PP.files
%{_libdir}/R/library/spatial/R/
# splines
%{_libdir}/R/library/splines/
# stats
%{_libdir}/R/library/stats/
# stats4
%{_libdir}/R/library/stats4/
# survival
%{_libdir}/R/library/survival/
# tcltk
%{_libdir}/R/library/tcltk/
# tools
%{_libdir}/R/library/tools/
# utils
%{_libdir}/R/library/utils/
%{_libdir}/R/modules
%{_libdir}/R/COPYING
# %{_libdir}/R/NEWS*
%{_libdir}/R/SVN-REVISION
/usr/lib/rpm/R-make-search-index.sh
%{_infodir}/R-*.info*
%{macrosdir}/macros.R
%{_mandir}/man1/*
%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
%docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
/etc/ld.so.conf.d/*

%files core-devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/libR.pc
%{_includedir}/R
# Symlink to %{_includedir}/R/
%{_libdir}/R/include

%files devel
# Nothing, all files provided by R-core-devel

%files java
# Nothing, all files provided by R-core

%files java-devel
# Nothing, all files provided by R-core-devel

%files -n libRmath
%defattr(-, root, root, -)
%doc doc/COPYING
%{_libdir}/libRmath.so

%files -n libRmath-devel
%defattr(-, root, root, -)
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

%files -n libRmath-static
%defattr(-, root, root, -)
%{_libdir}/libRmath.a

%clean
rm -rf ${RPM_BUILD_ROOT};

%post core
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
for doc in admin exts FAQ intro lang; do
   file=%{_infodir}/R-${doc}.info.gz
   if [ -e $file ]; then
      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null || :
   fi
done
/sbin/ldconfig
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0

# With 2.10.0, we no longer need to do any of this.

# Update package indices
# %__cat %{_libdir}/R/library/*/CONTENTS > %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute RHOME
# sed -i "s!../../..!%{_libdir}/R!g" %{_docdir}/R-%{version}/html/search/index.txt

# This could fail if there are no noarch R libraries on the system.
# %__cat %{_datadir}/R/library/*/CONTENTS >> %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null || exit 0
# Don't use .. based paths, substitute /usr/share/R
# sed -i "s!../../..!/usr/share/R!g" %{_docdir}/R-%{version}/html/search/index.txt


%preun core
if [ $1 = 0 ]; then
   # Delete directory entries for info files (if they were installed)
   for doc in admin exts FAQ intro lang; do
      file=%{_infodir}/R-${doc}.info.gz
      if [ -e ${file} ]; then
         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null || :
      fi
   done
fi

%postun core
/sbin/ldconfig

%post java
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0

%post java-devel
R CMD javareconf \
    JAVA_HOME=%{_jvmdir}/jre \
    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
    > /dev/null 2>&1 || exit 0

%post -n libRmath -p /sbin/ldconfig

%postun -n libRmath -p /sbin/ldconfig

%changelog
* Fri Dec 16 2016 sulit - 3.2.1-5
- rebuild

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 3.2.1-4
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.2.1-3
- Rebuild

