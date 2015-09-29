# Only a static library is provided, so no debug information can be extracted.
%global debug_package %{nil}

# This package uses assembly to do its work.  This is the entire list of
# supported architectures understood by RPM, even those not currently supported
# by Fedora.  RPM hasn't heard about line continuations, hence the mess.
%global ffcall_arches %{ix86} x86_64 amd64 %{alpha} armv3l armv4b armv4l armv4tl armv5tel armv5tejl armv6l armv7l armv7hl armv7hnl parisc hppa1.0 hppa1.1 hppa1.2 hppa2.0 ia64 m68k mips mipsel ppc ppc8260 ppc8560 ppc32dy4 ppciseries ppcpseries %{power64} s390 s390x %{sparc}

Name:           ffcall
Version:        1.10
Release:        18.20120424cvs%{?dist}
Summary:        Libraries for foreign function call interfaces

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.gnu.org/software/libffcall/
# There has been no official release for several years, and the project web
# site encourages use of a CVS snapshot.  Make the tarball as follows:
#   cvs -z3 -d:pserver:anonymous@cvs.savannah.gnu.org:/sources/libffcall 
#       export -D 2012-04-24 ffcall
#   tar cJf ffcall-20120424cvs.tar.xz ffcall
Source0:        %{name}-20120424cvs.tar.xz
# This patch will not be sent upstream.  It removes the possibility of using
# mprotect() to make memory executable, as that runs afoul of SELinux.
Patch0:         %{name}-trampoline.patch
# Upstream is dead, so this patch will not be sent.  Update some uses of OABI
# on ARM to their EABI equivalents.
Patch1:         %{name}-arm.patch

Provides:       %{name}-static = %{version}-%{release}

ExclusiveArch:  %{ffcall_arches}

%description
This is a collection of four libraries which can be used to build
foreign function call interfaces in embedded interpreters.  The four
packages are:
 - avcall: calling C functions with variable arguments
 - vacall: C functions accepting variable argument prototypes
 - trampoline: closures as first-class C functions
 - callback: closures with variable arguments as first-class C functions
   (a reentrant combination of vacall and trampoline)


%prep
%setup -q -n ffcall
%patch0
%patch1

# Remove prebuilt object files
find . -name \*.o | xargs rm -f

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC -DMAP_VARIABLE=2"
%configure
make # %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
make install DESTDIR=$RPM_BUILD_ROOT
rm -fr $RPM_BUILD_ROOT%{_datadir}/html
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd $RPM_BUILD_ROOT%{_mandir}/man3

# Advertise supported architectures
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat > $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.%{name} << EOF
# arches that ffcall supports
%%ffcall_arches %{ffcall_arches}
EOF

# Fix man pages with overly generic names (bz 800360)
for page in *; do
  mv $page %{name}-$page
done

%files
%license COPYING
%doc README NEWS
%doc avcall/avcall.html
%doc callback/callback.html
%doc callback/trampoline_r/trampoline_r.html
%doc trampoline/trampoline.html
%doc vacall/vacall.html
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/man*/*
%{_rpmconfigdir}/macros.d/macros.%{name}


%changelog
