# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%global commit c58038c56923

Name:           eigen3
Version:        3.2.6
Release:        3%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math

License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
# Source file is at: http://bitbucket.org/eigen/eigen/get/3.1.3.tar.bz2
# Renamed source file so it's not just a version number
Source0:        eigen-%{version}.tar.bz2

# Fix build with recent suitesparse versions
Patch0:         eigen-3.2.3_suitesparse.patch
# Install FindEigen3.cmake
# Adapted from Debian eigen3 package
Patch1:         01_install_FindEigen3.patch

BuildRequires:  atlas-devel
BuildRequires:  fftw-devel
BuildRequires:  libglew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
#BuildRequires:  sparsehash-devel
#BuildRequires:  suitesparse-devel
BuildRequires:  gcc-gfortran
#BuildRequires:  SuperLU-devel
#BuildRequires:  qt-devel

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz

%description
%{summary}.

%package devel
Summary:   A lightweight C++ template library for vector and matrix math
BuildArch: noarch
# -devel subpkg only atm, compat with other distros
Provides:  %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:  %{name}-static = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary:   Developer documentation for Eigen
Requires:  %{name}-devel = %{version}-%{release}
BuildArch: noarch
%description doc
Developer documentation for Eigen.

%prep
%setup -q -n eigen-eigen-%{commit}
%patch0 -p1
%patch1 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. -DBLAS_LIBRARIES="cblas"
popd

make -C %{_target_platform} %{?_smp_mflags}
make doc -C %{_target_platform} %{?_smp_mflags}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
%make_install -C %{_target_platform}

%check
# Run tests but make failures non-fatal. Note that upstream doesn't expect the
# tests to pass consistently since they're seeded randomly.
#make -C %{_target_platform} %{?_smp_mflags} buildtests
#make -C %{_target_platform} %{?_smp_mflags} test ARGS="-V" || exit 0

%files devel
%license COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%{_includedir}/eigen3
%{_datadir}/pkgconfig/*
%{_datadir}/cmake/Modules/*.cmake

%files doc
%doc %{_target_platform}/doc/html

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.2.6-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 3.2.6-2
- Initial build. 

