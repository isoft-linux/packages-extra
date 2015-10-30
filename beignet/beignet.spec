Name: beignet
Version: 1.1.1
Release: 7.llvm37.git%{?dist}
Epoch: 2
Summary: Open source implementation of the OpenCL for Intel GPUs

License: LGPLv2+
URL: https://01.org/beignet/
#Source0: https://01.org/sites/default/files/%{name}-%{version}-source.tar.gz

#git clone git://anongit.freedesktop.org/beignet
Source0: beignet.tar.gz

BuildRequires: cmake
BuildRequires: libllvm-devel >= 3.3 libclang-devel >= 3.3 libllvm-static >= 3.3
BuildRequires: libdrm-devel mesa-libGL-devel mesa-libEGL-devel mesa-libgbm-devel ocl-icd-devel
BuildRequires: zlib-devel libedit-devel
BuildRequires: opencl-headers
BuildRequires: git

BuildRequires: python3-devel


ExclusiveArch: x86_64 %{ix86}

%description
Beignet is an open source implementation of the OpenCL specification - a generic
compute oriented API. This code base contains the code to run OpenCL programs
on Intel GPUs which basically defines and implements the OpenCL host functions
required to initialize the device, create the command queues, the kernels and
the programs and run them on the GPU. 

%package devel
Summary: Open source implementation of the OpenCL for Intel GPUs devel package
Requires: opencl-headers
Requires: beignet = %{epoch}:%{version}-%{release}

%description devel
Devel package for Beignet is an open source implementation of the OpenCL
specification - a generic compute oriented API.

%prep
%setup -n beignet

%build
mkdir build
pushd build
 %cmake -DLLVM_INSTALL_DIR=%{_bindir} ..
 %make_build
popd

%install
pushd build
 %make_install
popd

find %{buildroot}%{_includedir}/CL/ -not -name "cl_intel.h" -type f -delete

%check
#the test passed 100%, but it may failed when driver changed.
source build/utests/setenv.sh
build/utests/utest_run ||:

%files
%license COPYING
%doc README.md
%{_libdir}/beignet/
%{_sysconfdir}/OpenCL/vendors/intel-beignet.icd

%files devel
%doc docs/*
%{_includedir}/CL/cl_intel.h

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2:1.1.1-7.llvm37.git
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to latest git.

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 1.1.1

