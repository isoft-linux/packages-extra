%define releasedate 20141204
%define major 4
%define minor 3
%define update 2
%define dotver %{major}.%{minor}
%define sourcebasename tbb%{major}%{minor}_%{releasedate}oss

%define sourcefilename %{sourcebasename}_src.tgz

Name:    tbb
Summary: The Threading Building Blocks library abstracts low-level threading details
Version: %{dotver}
Release: 2.%{releasedate}%{?dist}
License: GPLv2 with exceptions
URL:     http://threadingbuildingblocks.org/

Source0: http://threadingbuildingblocks.org/sites/default/files/software_releases/source/%{sourcebasename}_src.tgz
# These two are downstream sources.
Source6: tbb.pc
Source7: tbbmalloc.pc
Source8: tbbmalloc_proxy.pc

# Propagate CXXFLAGS variable into flags used when compiling C++.
# This so that RPM_OPT_FLAGS are respected.
Patch1: tbb-3.0-cxxflags.patch

# Replace mfence with xchg (for 32-bit builds only) so that TBB
# compiles and works supported hardware.  mfence was added with SSE2,
# which we still don't assume.
Patch2: tbb-4.0-mfence.patch

# Don't snip -Wall from C++ flags.  Add -fno-strict-aliasing, as that
# uncovers some static-aliasing warnings.
# Related: https://bugzilla.redhat.com/show_bug.cgi?id=1037347
Patch3: tbb-4.3-dont-snip-Wall.patch

BuildRequires: libstdc++-devel

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%package doc
Summary: The Threading Building Blocks documentation

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.


%prep
%setup -q -n %{sourcebasename}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" tbb_build_prefix=obj
for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    sed 's/_FEDORA_VERSION/%{major}.%{minor}.%{update}/' ${file} \
        > $(basename ${file})
done

%check
%ifarch ppc64le
make test
%endif

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}

pushd build/obj_release
    for file in libtbb{,malloc{,_proxy}}; do
        install -p -D -m 755 ${file}.so.2 $RPM_BUILD_ROOT/%{_libdir}
        ln -s $file.so.2 $RPM_BUILD_ROOT/%{_libdir}/$file.so
    done
popd

pushd include
    find tbb -type f ! -name \*.htm\* -exec \
        install -p -D -m 644 {} $RPM_BUILD_ROOT/%{_includedir}/{} \
    \;
popd

for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    install -p -D -m 644 $(basename ${file}) \
	$RPM_BUILD_ROOT/%{_libdir}/pkgconfig/$(basename ${file})
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING doc/Release_Notes.txt
%{_libdir}/*.so.2

%files devel
%doc CHANGES
%{_includedir}/tbb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc doc/Release_Notes.txt
%doc doc/html

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 4.3-2.20141204
- Initial build

