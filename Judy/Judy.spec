Name:		Judy
Version:	1.0.5
Release:	11%{?dist}
Summary:	General purpose dynamic array
License:	LGPLv2+
URL:		http://sourceforge.net/projects/judy/
Source0:	http://downloads.sf.net/judy/Judy-%{version}.tar.gz
# Make tests use shared instead of static libJudy
Patch0:		Judy-1.0.4-test-shared.patch
# The J1* man pages were incorrectly being symlinked to Judy, rather than Judy1
# This patch corrects that; submitted upstream 2008/11/27
Patch1:		Judy-1.0.4-fix-Judy1-mans.patch
# Fix some code with undefined behavior, commented on and removed by gcc
Patch2:		Judy-1.0.5-undefined-behavior.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

%description
Judy is a C library that provides a state-of-the-art core technology
that implements a sparse dynamic array. Judy arrays are declared
simply with a null pointer. A Judy array consumes memory only when it
is populated, yet can grow to take advantage of all available memory
if desired. Judy's key benefits are scalability, high performance, and
memory efficiency. A Judy array is extensible and can scale up to a
very large number of elements, bounded only by machine memory. Since
Judy is designed as an unbounded array, the size of a Judy array is
not pre-allocated but grows and shrinks dynamically with the array
population.

%package devel
Summary:	Development libraries and headers for Judy
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries and header files
for developing applications that use the Judy library.

%prep
%setup -q -n judy-%{version}
%patch0 -p1 -b .test-shared
%patch1 -p1 -b .fix-Judy1-mans
%patch2 -p1 -b .behavior

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -fno-tree-ccp -fno-tree-dominator-opts -fno-tree-copy-prop -fno-tree-vrp"
%configure --disable-static
make 
#%{?_smp_mflags}
# fails to compile properly with parallel make:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2129019&group_id=55753&atid=478138

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# get rid of static libs and libtool archives
rm -f %{buildroot}%{_libdir}/*.{a,la}
# clean out zero length and generated files from doc tree
rm -rf doc/man
rm -f doc/Makefile* doc/ext/README_deliver
[ -s doc/ext/COPYRIGHT ] || rm -f doc/ext/COPYRIGHT
[ -s doc/ext/LICENSE ] || rm -f doc/ext/LICENSE

%check
cd test
./Checkit
cd -

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README examples/
%{_libdir}/libJudy.so.*

%files devel
%defattr(-,root,root,-)
%doc doc
%{_includedir}/Judy.h
%{_libdir}/libJudy.so
%{_mandir}/man3/J*.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
