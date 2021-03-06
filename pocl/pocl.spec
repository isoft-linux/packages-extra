Name:		pocl
Version:	0.13
Release:	11.llvm37.git
Summary:	Portable Computing Language

License:	BSD
URL:		http://portablecl.org/
#git clone https://github.com/pocl/pocl
Source0:    %{name}.tar.xz
Patch0: pocl-build-with-llvm-3.8.patch

BuildRequires: autoconf automake libtool
BuildRequires: ocl-icd-devel, libhwloc-devel	
BuildRequires: libllvm-devel, libllvm-static, libclang-static, libclang-devel, libltdl-devel, ncurses-devel
BuildRequires: clang llvm
BuildRequires: pkgconfig sed grep
BuildRequires: mesa-libGL-devel libGLU-devel libglew-devel
BuildRequires: opencl-headers
BuildRequires: zlib-devel
BuildRequires: libedit-devel

Requires: ocl-icd, libhwloc

%description
Portable Computing Language (pocl) aims to become a MIT-licensed open source implementation of the OpenCL standard which can be easily adapted for new targets and devices, both for homogeneous CPU and heterogenous GPUs/accelerators.


%package devel 
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel 
This package contains the header files, static libraries and development
documentation for %{name}.

%prep
%setup -q -n %{name} 
%patch0 -p1

%build
export CC=clang
export CXX=clang++
%ifarch %{ix86}
export LLC_HOST_CPU="pentium-m"
%endif
%ifarch x86_64
export LLC_HOST_CPU="x86-64"
%endif

if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
    --disable-static \
    --enable-icd \
    --enable-tests-with-icd=default

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%check
#from git 953cdd7, these two test failure fixed.
#https://github.com/pocl/pocl/pull/271 
#24: Sampler address clamp                           FAILED (testsuite.at:264)
#25: Image query functions                           FAILED (testsuite.at:272)
make check

%files
%defattr(-,root,root,-)
%{_sysconfdir}/OpenCL/vendors/pocl.icd
%{_bindir}/pocl-standalone
%{_libdir}/libpocl*.so.*
%dir %{_datadir}/pocl
%{_datadir}/pocl/kernel-*-linux-gnu.bc
#these files belong to runtime, not devel package.
%dir %{_libdir}/pocl
%{_libdir}/pocl/*
%{_datadir}/pocl/include

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/pocl.pc

%changelog
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 0.13-11.llvm37.git
- Update and rebuild

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 0.13-10.llvm37.git
- Update, build with llvm-3.8

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 0.13-9.git
- Rebuild, bump version to 0.13 git.

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 0.12-8.git
- add more build requires

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 0.12-7.git
- update to git 953cdd7, fix image/samplers test failed issue.

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.12-6.git
- Rebuild

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 0.12-5.git
- update to c80bcc3

* Fri Sep 04 2015 Cjacker <cjacker@foxmail.com>
- update to latest git.
