# The library consists of headers only
%global debug_package %{nil}

Name:           glm
Version:        0.9.7.0
Release:        3%{?dist}
Summary:        C++ mathematics library for graphics programming

License:        MIT
URL:            http://glm.g-truc.net/
Source0:        https://github.com/g-truc/glm/releases/download/%{version}/%{name}-%{version}.zip
Patch0:         glm-0.9.5.2-smallercount.patch
Patch1:         glm-0.9.6.1-ulp.patch

BuildRequires:  cmake

%description
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%package        devel
Summary:        C++ mathematics library for graphics programming
BuildArch:      noarch

Provides:       %{name}-static = %{version}-%{release}

%description    devel
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%{name}-devel is only required for building software that uses
the GLM library. Because GLM currently is a header-only library,
there is no matching run time package.

%package        doc
Summary:        Documentation for %{name}-devel
BuildArch:      noarch

%description    doc
The %{name}-doc package contains reference documentation and
a programming manual for the %{name}-devel package.

%prep
# Some glm releases, like version 0.9.3.1, place contents of
# the source archive directly into the archive root. Others,
# like glm 0.9.3.2, place them into a single subdirectory.
# The former case is inconvenient, but it can be be
# compensated for with the -c option of the setup macro.
#
# When updating this package, take care to check if -c is
# needed for the particular version.
#
# Also it looks like some versions get shipped with a common
# directory in archive root, but with an unusual name for the
# directory. In this case, use the -n option of the setup macro.
%setup -q -n glm

# A couple of files had CRLF line-ends in them.
# Check with rpmlint after updating the package that we are not
# forgetting to convert line endings in some files.
#
# This release of glm seems to have shipped with no CRLF file
# endings at all, so these are commented out.
sed -i 's/\r//' copying.txt
sed -i 's/\r//' readme.md
sed -i 's/\r//' doc/api/doxygen.css
sed -i 's/\r//' doc/api/dynsections.js
sed -i 's/\r//' doc/api/jquery.js
sed -i 's/\r//' doc/api/tabs.css


%patch0 -p1 -b .smallercount
%patch1 -p1 -b .ulp

#it's a provided module
rm -rf cmake/GNUInstallDirs.cmake
%build
mkdir build
cd build
%{cmake} -DGLM_TEST_ENABLE=ON ..
make %{?_smp_mflags}

%check
cd build

# Some tests are disabled due to known upstream bugs:
# https://github.com/g-truc/glm/issues/212
# https://github.com/g-truc/glm/issues/296
ctest --output-on-failure -E '(test-gtc_packing|test-gtc_integer)'

%install
cd build

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name CMakeLists.txt -exec rm -f {} ';'

%files devel
%doc copying.txt readme.md
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}

%files doc
%doc copying.txt
%doc doc/%{name}.pdf
%doc doc/api/

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.9.7.0-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.9.7.0-2
- Initial build. 

