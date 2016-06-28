Name: yajl
Version: 2.1.0
Release: 5
Summary: Yet Another JSON Library (YAJL)

Group: Development/Libraries
License: ISC
URL: http://lloyd.github.com/yajl/

#
# NB, upstream does not provide pre-built tar.gz downloads. Instead
# they make you use the 'on the fly' generated tar.gz from GITHub's
# web interface
#
# The Source0 for any version is obtained by a URL
#
#   https://github.com/lloyd/yajl/releases/tag/2.1.0
#
Source0: %{name}-%{version}.tar.gz
Patch1: %{name}-%{version}-pkgconfig-location.patch
Patch2: %{name}-%{version}-pkgconfig-includedir.patch
Patch3: %{name}-%{version}-test-location.patch
Patch4: %{name}-%{version}-dynlink-binaries.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Requires: %{name} = %{version}-%{release}

%description
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

%description devel
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
mkdir build
cd build
%cmake ..
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT


# No static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/libyajl_s.a


%check
cd test
(cd parsing && ./run_tests.sh)
(cd api && ./run_tests.sh)

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.2
%{_libdir}/libyajl.so.2.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{_includedir}/yajl
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_includedir}/yajl/yajl_tree.h
%{_includedir}/yajl/yajl_version.h
%{_libdir}/libyajl.so
%{_libdir}/pkgconfig/yajl.pc


%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.1.0-5
- rebuilt for libvirt

