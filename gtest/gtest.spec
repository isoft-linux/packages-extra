Summary:        Google C++ testing framework
Name:           gtest
Version:        1.7.0
Release:        6%{?dist}
License:        BSD
URL:            http://code.google.com/p/googletest/
Source0:        http://googletest.googlecode.com/files/gtest-%{version}.zip
Patch0:         gtest-soname.patch
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  python-devel

%description
Google's framework for writing C++ tests on a variety of platforms
(GNU/Linux, Mac OS X, Windows, Windows CE, and Symbian). Based on the
xUnit architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%package        devel
Summary:        Development files for %{name}
Requires:       automake
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%setup -q
%patch0 -p1 -b .0-soname

# keep a clean copy of samples.
cp -a ./samples ./samples.orig

%build
# this is odd but needed only to generate gtest-config.
%configure
mkdir build && pushd build
%cmake -DBUILD_SHARED_LIBS=ON \
       -DCMAKE_SKIP_BUILD_RPATH=TRUE \
       -DPYTHON_EXECUTABLE=%{__python2} \
       -Dgtest_build_tests=ON ..
make %{?_smp_mflags}

%check
# LD_LIBRARY_PATH needed due to cmake_skip_rpath in %%build
pushd build
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/build make test
popd

# Restore the clean copy of samples.
# To be later listed against doc.
rm -rf ./samples
mv ./samples.orig ./samples

%install
# make install doesn't work anymore.
# need to install them manually.
install -d %{buildroot}{%{_includedir}/gtest{,/internal},%{_libdir}}
# just for backward compatibility
install -p -m 0755 build/libgtest.so.*.* build/libgtest_main.so.*.* %{buildroot}%{_libdir}/
(cd %{buildroot}%{_libdir};
ln -sf libgtest.so.*.* %{buildroot}%{_libdir}/libgtest.so
ln -sf libgtest_main.so.*.* %{buildroot}%{_libdir}/libgtest_main.so
)
/sbin/ldconfig -n %{buildroot}%{_libdir}
install -D -p -m 0755 scripts/gtest-config %{buildroot}%{_bindir}/gtest-config
install -p -m 0644 include/gtest/*.h %{buildroot}%{_includedir}/gtest/
install -p -m 0644 include/gtest/internal/*.h %{buildroot}%{_includedir}/gtest/internal/
install -D -p -m 0644 m4/gtest.m4 %{buildroot}%{_datadir}/aclocal/gtest.m4

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGES CONTRIBUTORS LICENSE README
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files devel
%doc samples
%{_bindir}/gtest-config
%{_datadir}/aclocal/gtest.m4
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_includedir}/gtest

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.7.0-6
- Rebuild

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build.

