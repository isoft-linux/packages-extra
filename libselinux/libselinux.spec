%if 0%{?fedora} > 12
%global with_python3 1
%endif

%define ruby_inc %(pkg-config --cflags ruby)
%define libsepolver 2.4-1
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: SELinux library and simple utilities
Name: libselinux
Version: 2.4
Release: 6
License: Public Domain
Group: System Environment/Libraries
# https://github.com/SELinuxProject/selinux/wiki/Releases
Source: https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20150202/%{name}-%{version}.tar.gz
Source1: selinuxconlist.8
Source2: selinuxdefcon.8
Url: https://github.com/SELinuxProject/selinux/wiki
# use make-rhat-patches.sh to create following patches from https://github.com/fedora-selinux/selinux/
# HEAD https://github.com/fedora-selinux/selinux/commit/8c09d34e464e79a602fb9c9408554279aede3b6b
Patch1: libselinux-rhat.patch
BuildRequires: pkgconfig python-devel ruby-devel ruby libsepol-static >= %{libsepolver} swig pcre-devel xz-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3
Requires: libsepol%{?_isa} >= %{libsepolver} pcre
Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package utils
Summary: SELinux libselinux utilies
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The libselinux-utils package contains the utilities

%package python
Summary: SELinux python bindings for libselinux
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python
The libselinux-python package contains the python bindings for developing 
SELinux applications. 

%if 0%{?with_python3}
%package python3
Summary: SELinux python 3 bindings for libselinux
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python3
The libselinux-python3 package contains python 3 bindings for developing
SELinux applications. 
%endif # with_python3

%package devel
Summary: Header files and libraries used to build SELinux
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libsepol-devel%{?_isa} >= %{libsepolver}

%description devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications. 

%package static
Summary: Static libraries used to build SELinux
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libselinux-static package contains the static libraries
needed for developing SELinux applications. 

%prep
%setup -q
%patch1 -p1 -b .rhat

%build
export LDFLAGS="%{?__global_ldflags}"

# To support building the Python wrapper against multiple Python runtimes
# Define a function, for how to perform a "build" of the python wrapper against
# a specific runtime:
BuildPythonWrapper() {
  BinaryName=$1

  # Perform the build from the upstream Makefile:
  make \
    PYTHON=$BinaryName \
    LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} \
    pywrap
}

make clean
make LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} swigify
make LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} all

BuildPythonWrapper %{__python}
%if 0%{?with_python3}
BuildPythonWrapper %{__python3}
%endif # with_python3

make RUBYINC="%{ruby_inc}" SHLIBDIR="%{_libdir}" LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} rubywrap

%install
InstallPythonWrapper() {
  BinaryName=$1

  make \
    PYTHON=$BinaryName \
    LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} \
    pywrap

  make \
    PYTHON=$BinaryName \
    DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" \
    SHLIBDIR="%{buildroot}/%{_lib}" BINDIR="%{buildroot}%{_bindir}" \
    SBINDIR="%{buildroot}%{_sbindir}" \
    install-pywrap
}

rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}/lib/tmpfiles.d
mkdir -p %{buildroot}/%{_libdir} 
mkdir -p %{buildroot}%{_includedir} 
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/var/run/setrans
echo "d /var/run/setrans 0755 root root" > %{buildroot}/%{_prefix}/lib/tmpfiles.d/libselinux.conf

InstallPythonWrapper %{__python}
%if 0%{?with_python3}
InstallPythonWrapper %{__python3}
%endif # with_python3

make DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}%{_libdir}" BINDIR="%{buildroot}%{_bindir}" SBINDIR="%{buildroot}%{_sbindir}" RUBYINSTALL=%{buildroot}%{ruby_vendorarchdir} install install-rubywrap

# Nuke the files we don't want to distribute
rm -f %{buildroot}%{_sbindir}/compute_*
rm -f %{buildroot}%{_sbindir}/deftype
rm -f %{buildroot}%{_sbindir}/execcon
rm -f %{buildroot}%{_sbindir}/getenforcemode
rm -f %{buildroot}%{_sbindir}/getfilecon
rm -f %{buildroot}%{_sbindir}/getpidcon
rm -f %{buildroot}%{_sbindir}/mkdircon
rm -f %{buildroot}%{_sbindir}/policyvers
rm -f %{buildroot}%{_sbindir}/setfilecon
rm -f %{buildroot}%{_sbindir}/selinuxconfig
rm -f %{buildroot}%{_sbindir}/selinuxdisable
rm -f %{buildroot}%{_sbindir}/getseuser
rm -f %{buildroot}%{_sbindir}/togglesebool
rm -f %{buildroot}%{_sbindir}/selinux_check_securetty_context
mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/
rm -f %{buildroot}%{_mandir}/man8/togglesebool*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libselinux.so.*
%ghost /var/run/setrans
%{_sbindir}/sefcontext_compile
%{_prefix}/lib/tmpfiles.d/libselinux.conf

%files utils
%defattr(-,root,root,-)
%{_sbindir}/avcstat
%{_sbindir}/getenforce
%{_sbindir}/getsebool
%{_sbindir}/matchpathcon
%{_sbindir}/selinuxconlist
%{_sbindir}/selinuxdefcon
%{_sbindir}/selinuxexeccon
%{_sbindir}/selinuxenabled
%{_sbindir}/setenforce
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_libdir}/golang/src/pkg/github.com/selinux
%{_libdir}/golang/src/pkg/github.com/selinux/selinux.go
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files static
%defattr(-,root,root,-)
%{_libdir}/libselinux.a

%files python
%defattr(-,root,root,-)
%dir %{python_sitearch}/selinux
%{python_sitearch}/selinux/*

%if 0%{?with_python3}
%files python3
%defattr(-,root,root,-)
%dir %{python3_sitearch}/selinux
%dir %{python3_sitearch}/selinux/__pycache__
%{python3_sitearch}/selinux/*.py*
%{python3_sitearch}/selinux/*.so
%{python3_sitearch}/selinux/__pycache__/*
%endif with_python3


%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 2.4-6
- rebuilt for libvirt. remove ruby.

