%bcond_without atlas310

%if %{with atlas310}
%global atlaslibs -lsatlas
%else
%global atlaslibs -lcblas -llapack
%endif

Name:           suitesparse
Version:        4.3.1
Release:        5%{?dist}
Summary:        A collection of sparse matrix libraries

License:        LGPLv2+ and GPLv2+
URL:            http://www.cise.ufl.edu/research/sparse/SuiteSparse
Source0:        http://www.cise.ufl.edu/research/sparse/SuiteSparse/SuiteSparse-%{version}.tar.gz
# Move #include <math.h> out of StuiteSparse_config.h and into SuiteSparse_config.c
Patch0:         suitesparse-math.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with atlas310}
BuildRequires:  atlas-devel >= 3.10
%else
BuildRequires:  atlas-devel
%endif
%ifnarch s390 s390x
BuildRequires:  tbb-devel
%global with_tbb 1
%endif

BuildRequires:  hardlink

Obsoletes:      umfpack <= 5.0.1
Obsoletes:      ufsparse <= 2.1.1
Provides:       ufsparse = %{version}-%{release}

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD                 approximate minimum degree ordering
  BTF                 permutation to block triangular form (beta)
  CAMD                constrained approximate minimum degree ordering
  COLAMD              column approximate minimum degree ordering
  CCOLAMD             constrained column approximate minimum degree ordering
  CHOLMOD             sparse Cholesky factorization
  CSparse             a concise sparse matrix package
  CXSparse            CSparse extended: complex matrix, int and long int support
  KLU                 sparse LU factorization, primarily for circuit simulation
  LDL                 a simple LDL factorization
  SQPR                a multithread, multifrontal, rank-revealing sparse QR
                      factorization method
  UMFPACK             sparse LU factorization
  SuiteSparse_config  configuration file for all the above packages.
  RBio                read/write files in Rutherford/Boeing format


%package devel
Summary:        Development headers for SuiteSparse
Requires:       %{name} = %{version}-%{release}
Obsoletes:      umfpack-devel <= 5.0.1
Obsoletes:      ufsparse-devel <= 2.1.1
Provides:       ufsparse-devel = %{version}-%{release}

%description devel
The suitesparse-devel package contains files needed for developing
applications which use the suitesparse libraries.


%package static
Summary:        Static version of SuiteSparse libraries
Requires:       %{name}-devel = %{version}-%{release}
Provides:       ufsparse-static = %{version}-%{release}

%description static
The suitesparse-static package contains the statically linkable
version of the suitesparse libraries.

%package doc
Summary:        Documentation files for SuiteSparse
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.


%prep
%setup -q -n SuiteSparse
%patch0 -p1 -b .math

%build
%define amd_version 2.4.0
%define amd_version_major 2
%define btf_version 1.2.0
%define btf_version_major 1
%define camd_version 2.4.0
%define camd_version_major 2
%define ccolamd_version 2.9.0
%define ccolamd_version_major 2
%define cholmod_version 3.0.1
%define cholmod_version_major 3
%define colamd_version 2.9.0
%define colamd_version_major 2
%define csparse_version 3.1.3
%define csparse_version_major 3
%define cxsparse_version 3.1.3
%define cxsparse_version_major 3
%define klu_version 1.3.0
%define klu_version_major 1
%define ldl_version 2.2.0
%define ldl_version_major 2
%define rbio_version 2.2.0
%define rbio_version_major 2
%define spqr_version 1.3.3
%define spqr_version_major 1
%define SuiteSparse_config_ver 4.3.1
%define SuiteSparse_config_major 4
%define umfpack_version 5.7.0
%define umfpack_version_major 5
### CHOLMOD can also be compiled to use the METIS library, but it is not
### used here because its licensing terms exclude it from Fedora Extras.
### To compile with METIS, define enable_metis as 1 below.
%define enable_metis 0
### CXSparse is a superset of CSparse, and the two share common header
### names, so it does not make sense to build both. CXSparse is built
### by default, but CSparse can be built instead by defining
### enable_csparse as 1 below.
%define enable_csparse 0

mkdir -p Doc/{AMD,BTF,CAMD,CCOLAMD,CHOLMOD,COLAMD,KLU,LDL,UMFPACK,SPQR,RBio} Lib Include

# SuiteSparse_config needs to come first
pushd SuiteSparse_config
  make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  ar x libsuitesparseconfig.a
  pushd ../Lib
    gcc -shared -Wl,-soname,libsuitesparseconfig.so.%{SuiteSparse_config_major} -o \
        libsuitesparseconfig.so.%{SuiteSparse_config_ver} ../SuiteSparse_config/*.o -lm
    ln -sf libsuitesparseconfig.so.%{SuiteSparse_config_ver} libsuitesparseconfig.so.%{SuiteSparse_config_major}
    ln -sf libsuitesparseconfig.so.%{SuiteSparse_config_ver} libsuitesparseconfig.so
    cp -p ../SuiteSparse_config/*.a ./
  popd
  cp -p *.h ../Include
popd

pushd AMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libamd.so.%{amd_version_major} -o \
        libamd.so.%{amd_version} ../AMD/Lib/*.o \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libamd.so.%{amd_version} libamd.so.%{amd_version_major}
    ln -sf libamd.so.%{amd_version} libamd.so
    cp -p ../AMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/*.pdf ../Doc/AMD
popd

pushd BTF
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libbtf.so.%{btf_version_major} -o \
        libbtf.so.%{btf_version} ../BTF/Lib/*.o
    ln -sf libbtf.so.%{btf_version} libbtf.so.%{btf_version_major}
    ln -sf libbtf.so.%{btf_version} libbtf.so
    cp -p ../BTF/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/BTF
popd

pushd CAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcamd.so.%{camd_version_major} -o \
        libcamd.so.%{camd_version} ../CAMD/Lib/*.o \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libcamd.so.%{camd_version} libcamd.so.%{camd_version_major}
    ln -sf libcamd.so.%{camd_version} libcamd.so
    cp -p ../CAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/License Doc/*.pdf ../Doc/CAMD
popd

pushd CCOLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libccolamd.so.%{ccolamd_version_major} -o \
        libccolamd.so.%{ccolamd_version} ../CCOLAMD/Lib/*.o \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libccolamd.so.%{ccolamd_version} libccolamd.so.%{ccolamd_version_major}
    ln -sf libccolamd.so.%{ccolamd_version} libccolamd.so
    cp -p ../CCOLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/CCOLAMD
popd

pushd COLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcolamd.so.%{colamd_version_major} -o \
        libcolamd.so.%{colamd_version} ../COLAMD/Lib/*.o \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libcolamd.so.%{colamd_version} libcolamd.so.%{colamd_version_major}
    ln -sf libcolamd.so.%{colamd_version} libcolamd.so
    cp -p ../COLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/COLAMD
popd

%if "%{?enable_metis}" == "1"
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -I%{_includedir}/metis -fPIC"
%else
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -DNPARTITION -fPIC"
%endif
pushd CHOLMOD
  pushd Lib
    make CFLAGS="$CHOLMOD_FLAGS"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcholmod.so.%{cholmod_version_major} -o \
        libcholmod.so.%{cholmod_version} ../CHOLMOD/Lib/*.o \
        -L%{_libdir}/atlas %{atlaslibs} \
        libamd.so.%{amd_version_major} \
        libcamd.so.%{camd_version_major} libcolamd.so.%{colamd_version_major} \
        libccolamd.so.%{ccolamd_version_major} \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libcholmod.so.%{cholmod_version} libcholmod.so.%{cholmod_version_major}
    ln -sf libcholmod.so.%{cholmod_version} libcholmod.so
    cp -p ../CHOLMOD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/*.pdf ../Doc/CHOLMOD
  cp -p Cholesky/License.txt ../Doc/CHOLMOD/Cholesky_License.txt
  cp -p Core/License.txt ../Doc/CHOLMOD/Core_License.txt
  cp -p MatrixOps/License.txt ../Doc/CHOLMOD/MatrixOps_License.txt
  cp -p Partition/License.txt ../Doc/CHOLMOD/Partition_License.txt
  cp -p Supernodal/License.txt ../Doc/CHOLMOD/Supernodal_License.txt
popd

%if "%{?enable_csparse}" == "1"
pushd CSparse
  pushd Source
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
    cp -p cs.h ../../Include
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcsparse.so.%{csparse_version_major} -o \
        libcsparse.so.%{csparse_version} ../CSparse/Source/*.o -lm
    ln -sf libcsparse.so.%{csparse_version} libcsparse.so.%{csparse_version_major}
    ln -sf libcsparse.so.%{csparse_version} libcsparse.so
    cp -p ../CSparse/Source/*.a ./
  popd
  mkdir ../Doc/CSparse/
  cp -p Doc/* ../Doc/CSparse
popd

%else
pushd CXSparse
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libcxsparse.so.%{cxsparse_version_major} -o \
        libcxsparse.so.%{cxsparse_version} ../CXSparse/Lib/*.o -lm
    ln -sf libcxsparse.so.%{cxsparse_version} libcxsparse.so.%{cxsparse_version_major}
    ln -sf libcxsparse.so.%{cxsparse_version} libcxsparse.so
    cp -p ../CXSparse/Lib/*.a ./
  popd
  cp -p Include/cs.h ../Include
  mkdir ../Doc/CXSparse/
  cp -p Doc/* ../Doc/CXSparse
popd
%endif

pushd KLU
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libklu.so.%{klu_version_major} -o \
        libklu.so.%{klu_version} ../KLU/Lib/*.o \
        libamd.so.%{amd_version_major} libcolamd.so.%{colamd_version_major} \
        libbtf.so.%{btf_version_major} \
        libsuitesparseconfig.so.%{SuiteSparse_config_major}
    ln -sf libklu.so.%{klu_version} libklu.so.%{klu_version_major}
    ln -sf libklu.so.%{klu_version} libklu.so
    cp -p ../KLU/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/lesser.txt ../Doc/KLU
popd

pushd LDL
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libldl.so.%{ldl_version_major} -o \
        libldl.so.%{ldl_version} ../LDL/Lib/*.o
    ln -sf libldl.so.%{ldl_version} libldl.so.%{ldl_version_major}
    ln -sf libldl.so.%{ldl_version} libldl.so
    cp -p ../LDL/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/lesser.txt Doc/*.pdf ../Doc/LDL
popd

pushd UMFPACK
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC" 
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,libumfpack.so.%{umfpack_version_major} -o \
        libumfpack.so.%{umfpack_version} ../UMFPACK/Lib/*.o \
        -L%{_libdir}/atlas %{atlaslibs} \
        libamd.so.%{amd_version_major} \
        libcholmod.so.%{cholmod_version_major} \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libumfpack.so.%{umfpack_version} libumfpack.so.%{umfpack_version_major}
    ln -sf libumfpack.so.%{umfpack_version} libumfpack.so
    cp -p ../UMFPACK/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/gpl.txt Doc/*.pdf ../Doc/UMFPACK
popd

pushd SPQR
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS %{?with_tbb:-DHAVE_TBB} -DNPARTITION -fPIC"
  popd
  pushd ../Lib
    g++ -shared -Wl,-soname,libspqr.so.%{spqr_version_major} -o \
        libspqr.so.%{spqr_version} ../SPQR/Lib/*.o \
        -L%{_libdir}/atlas -L%{_libdir} %{atlaslibs} \
        %{?with_tbb:-ltbb} \
        libcholmod.so.%{cholmod_version_major} \
        libsuitesparseconfig.so.%{SuiteSparse_config_major} -lm
    ln -sf libspqr.so.%{spqr_version} libspqr.so.%{spqr_version_major}
    ln -sf libspqr.so.%{spqr_version} libspqr.so
    cp -p ../SPQR/Lib/*.a ./
  popd
  cp -p Include/*.h* ../Include
  cp -p README{,_SPQR}.txt
  cp -p README_SPQR.txt Doc/* ../Doc/SPQR
popd

pushd RBio
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fPIC"
  popd
  pushd ../Lib
    gcc -shared -Wl,-soname,librbio.so.%{rbio_version_major} -o \
        librbio.so.%{rbio_version} ../RBio/Lib/*.o \
        libsuitesparseconfig.so.%{SuiteSparse_config_major}
    ln -sf librbio.so.%{rbio_version} librbio.so.%{rbio_version_major}
    ln -sf librbio.so.%{rbio_version} librbio.so
    cp -p ../RBio/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/License.txt ../Doc/RBio
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
pushd Lib
  for f in *.a *.so*; do
    cp -a $f ${RPM_BUILD_ROOT}%{_libdir}/$f
  done
popd
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/*.so.*
pushd Include
  for f in *.h *.hpp;  do
    cp -a $f ${RPM_BUILD_ROOT}%{_includedir}/%{name}/$f
  done
popd

# collect licenses in one place to ship as base package documentation
rm -rf Licenses
mkdir Licenses
find */ -iname lesser.txt -o -iname license.txt -o -iname gpl.txt -o \
    -iname license | while read f; do
        b="${f%%/*}"
        r="${f#$b}"
        x="$(echo "$r" | sed 's|/doc/|/|gi')"
        install -m0644 -D "$f" "./Licenses/$b/$x"
    done

# hardlink duplicate documentation files
hardlink -cv Docs/ Licenses/

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc Licenses
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/lib*.so

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,root)
%doc Doc/*

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 4.3.1-5
- Initial build

