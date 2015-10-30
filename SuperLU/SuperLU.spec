Name:			SuperLU
Version:		4.3
Release:		13%{?dist}
Summary:		Subroutines to solve sparse linear systems

License:		BSD
URL:			http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0:		http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_%{version}.tar.gz
# Build with -fPIC
Patch0:			%{name}-add-fpic.patch
# Build shared library
Patch1:			%{name}-build-shared-lib3.patch
# Fixes FTBFS if "-Werror=format-security" flag is used (#1037343)
Patch2:			%{name}-fix-format-security.patch
# Fixes testsuite
Patch3:			SuperLU-fix-testsuite.patch
# remove non-free mc64 functionality
# patch obtained from the debian package
Patch4:			SuperLU-removemc64.patch

BuildRequires:		atlas-devel
BuildRequires:		csh

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package devel
Summary:		Header files and libraries for SuperLU development
Requires:		%{name}%{?_isa}		=  %{version}-%{release}
Requires:	pkgconfig

%description devel 
The %{name}-devel package contains the header files
and libraries for use with %{name} package.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4

rm -fr SRC/mc64ad.f.bak
rm FORTRAN/*.old FORTRAN/*.bak
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done
cp -p MAKE_INC/make.linux make.inc
sed -i	-e "s|-O3|$RPM_OPT_FLAGS|"							\
	-e "s|\$(SUPERLULIB) ||"							\
	-e "s|\$(HOME)/Codes/%{name}_%{version}|%{_builddir}/%{name}_%{version}|"	\
	-e 's!lib/libsuperlu_4.3.a$!SRC/libsuperlu.so!'					\
	-e 's!-shared!& %{__global_ldflags}!'						\
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lsatlas|"				\
	make.inc

%build
make %{?_smp_mflags} superlulib
make -C TESTING

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%check
pushd TESTING
for _test in c d s z
do
  chmod +x ${_test}test.csh
  ./${_test}test.csh
done
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/libsuperlu.so.*

%files devel
%doc DOC EXAMPLE FORTRAN
%{_includedir}/%{name}/
%{_libdir}/libsuperlu.so

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 4.3-13
- Initial build

