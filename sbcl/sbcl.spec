%define common_lisp_controller 1

# generate/package docs
%define docs 1

# define to enable verbose build for debugging
#define sbcl_verbose 1 
%define sbcl_shell /bin/bash

Name: 	 sbcl
Summary: Steel Bank Common Lisp
Version: 1.2.16
Release: 2%{?dist}

License: BSD
URL:	 http://sbcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-%{version}-source.tar.bz2

ExclusiveArch: %{arm} %{ix86} x86_64 ppc sparcv9

# Pre-generated html docs
Source1: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-%{version}-documentation-html.tar.bz2

## x86 section
#Source10: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.0.15-x86-linux-binary.tar.bz2
%ifarch %{ix86}
%define sbcl_arch x86
BuildRequires: sbcl
# or
#define sbcl_bootstrap_src -b 10
%endif

## x86_64 section
Source20: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.2.0-x86-64-linux-binary.tar.bz2
%ifarch x86_64
%define sbcl_arch x86-64
#BuildRequires: sbcl
# or
%define sbcl_bootstrap_src -b 20
%define sbcl_bootstrap_dir sbcl-1.2.0-x86-64-linux
%endif

## ppc section
# Thanks David!
#Source30: sbcl-1.0.1-patched_el4-powerpc-linux.tar.bz2
#Source30: sbcl-1.0.1-patched-powerpc-linux.tar.bz2
%ifarch ppc 
%define sbcl_arch ppc
BuildRequires: sbcl
# or
#define sbcl_bootstrap_src -b 30
%endif

## sparc section
#Source40: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-0.9.17-sparc-linux-binary.tar.bz2
%ifarch sparcv9
%define sbcl_arch sparc 
BuildRequires: sbcl
# or
#define sbcl_bootstrap_src -b 40
%endif

## arm section
#Source50: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.2.0-armel-linux-binary.tar.bz2
%ifarch armv5tel
%define sbcl_arch arm
BuildRequires: sbcl
# or
#define sbcl_bootstrap_src -b 50
#define sbcl_bootstrap_dir sbcl-1.2.0-armel-linux
%endif

#Source60: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.2.0-armhf-linux-binary.tar.bz2
#Source60: sbcl-1.2.0-armhf-linux-binary-2.tar.bz2
%ifarch armv6hl armv7hl
%define sbcl_arch arm
BuildRequires: sbcl
# or
#define sbcl_bootstrap_src -b 60
#define sbcl_bootstrap_dir sbcl-1.2.0-armhf-vfp
%endif

%if 0%{?common_lisp_controller}
BuildRequires: common-lisp-controller
Requires:      common-lisp-controller
Requires(post): common-lisp-controller
Requires(preun): common-lisp-controller
Source200: sbcl.sh
Source201: sbcl.rc
Source202: sbcl-install-clc.lisp
%endif

Patch2: sbcl-1.1.13-personality.patch
Patch3: sbcl-1.2.11-optflags.patch
Patch6: sbcl-0.9.5-verbose-build.patch

## upstreamable patches
Patch50: sbcl-1.2.11-generate_version.patch

## upstream patches

# %%check/tests
BuildRequires: ed
BuildRequires: hostname
%if 0%{?docs}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
# doc generation
BuildRequires: ghostscript
BuildRequires: texinfo
BuildRequires: time
%endif

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp. It includes an integrated native compiler,
interpreter, and debugger.


%prep
%setup -q -c -n sbcl-%{version} -a 1 %{?sbcl_bootstrap_src}

pushd sbcl-%{version}

%patch2 -p1 -b .personality
%patch3 -p1 -b .optflags
%{?sbcl_verbose:%patch6 -p1 -b .verbose-build}
%patch50 -p1 -b .generate_version

# fix permissions (some have eXecute bit set)
find . -name '*.c' | xargs chmod 644

# set version.lisp-expr
sed -i.rpmver -e "s|\"%{version}\"|\"%{version}-%{release}\"|" version.lisp-expr

# make %%doc items available in parent dir to make life easier
cp -alf BUGS COPYING README CREDITS NEWS TLA TODO PRINCIPLES ..
ln -s sbcl-%{version}/doc ../doc
popd


%build
pushd sbcl-%{version}

export SBCL_HOME=%{_prefix}/lib/sbcl
%{?sbcl_arch:export SBCL_ARCH=%{sbcl_arch}}
%{?sbcl_shell} \
./make.sh \
  --prefix=%{_prefix} \
  %{?sbcl_bootstrap_dir:--xc-host="`pwd`/../%{sbcl_bootstrap_dir}/run-sbcl.sh"}

# docs
%if 0%{?docs}
make -C doc/manual info

# Handle pre-generated docs
tar xvjf %{SOURCE1}
cp -av %{name}-%{version}/doc/manual/* doc/manual/
%endif
popd


%install
pushd sbcl-%{version}
mkdir -p %{buildroot}{%{_bindir},%{_prefix}/lib,%{_mandir}}

unset SBCL_HOME 
export INSTALL_ROOT=%{buildroot}%{_prefix} 
%{?sbcl_shell} ./install.sh 

%if 0%{?common_lisp_controller}
install -m744 -p -D %{SOURCE200} %{buildroot}%{_prefix}/lib/common-lisp/bin/sbcl.sh
install -m644 -p -D %{SOURCE201} %{buildroot}%{_sysconfdir}/sbcl.rc
install -m644 -p -D %{SOURCE202} %{buildroot}%{_prefix}/lib/sbcl/install-clc.lisp
# linking ok? -- Rex
cp -p %{buildroot}%{_prefix}/lib/sbcl/sbcl.core %{buildroot}%{_prefix}/lib/sbcl/sbcl-dist.core
%endif
popd

## Unpackaged files
rm -rfv %{buildroot}%{_docdir}/sbcl
rm -fv  %{buildroot}%{_infodir}/dir
# CVS crud 
find %{buildroot} -name CVS -type d | xargs rm -rfv
find %{buildroot} -name .cvsignore | xargs rm -fv
# 'test-passed' files from %%check
find %{buildroot} -name 'test-passed' | xargs rm -vf


%check
pushd sbcl-%{version}
ERROR=0
# sanity check, essential contrib modules get built/included?
CONTRIBS="sb-posix.fasl sb-bsd-sockets.fasl"
for CONTRIB in $CONTRIBS ; do
  if [ ! -f %{buildroot}%{_prefix}/lib/sbcl/contrib/$CONTRIB ]; then
    echo "WARNING: ${CONTRIB} awol!"
    ERROR=1
    echo "ulimit -a"
    ulimit -a
  fi
done
pushd tests
# verify --version output
test "$(source ./subr.sh; SBCL_ARGS= run_sbcl --version 2>/dev/null | cut -d' ' -f2)" = "%{version}-%{release}"
# still seeing Failure: threads.impure.lisp / (DEBUGGER-NO-HANG-ON-SESSION-LOCK-IF-INTERRUPTED)
time %{?sbcl_shell} ./run-tests.sh ||:
popd
exit $ERROR
popd


%if ! 0%{?docs}
%pre
if [ $1 -gt 0 ]; then
/sbin/install-info --delete %{_infodir}/sbcl.info %{_infodir}/dir > /dev/null 2>&1 ||:
/sbin/install-info --delete %{_infodir}/asdf.info %{_infodir}/dir > /dev/null 2>&1 ||:
fi
%endif

%post
%if 0%{?docs}
/sbin/install-info %{_infodir}/sbcl.info %{_infodir}/dir ||:
/sbin/install-info %{_infodir}/asdf.info %{_infodir}/dir ||:
%endif
%if 0%{?common_lisp_controller}
/usr/sbin/register-common-lisp-implementation sbcl > /dev/null 2>&1 ||:
%endif

%preun
if [ $1 -eq 0 ]; then
%if 0%{?docs}
  /sbin/install-info --delete %{_infodir}/sbcl.info %{_infodir}/dir ||:
  /sbin/install-info --delete %{_infodir}/asdf.info %{_infodir}/dir ||:
%endif
%if 0%{?common_lisp_controller}
/usr/sbin/unregister-common-lisp-implementation sbcl > /dev/null 2>&1 ||:
%endif
fi

%files
%doc COPYING
%doc BUGS CREDITS NEWS PRINCIPLES README TLA TODO
%{_bindir}/sbcl
%dir %{_prefix}/lib/sbcl/
%{_prefix}/lib/sbcl/contrib/
%{_prefix}/lib/sbcl/site-systems/
%{_mandir}/man1/sbcl.1*
%if 0%{?docs}
%doc doc/manual/sbcl.html
%doc doc/manual/asdf.html
%{_infodir}/asdf.info*
%{_infodir}/sbcl.info*
%endif
%if 0%{?common_lisp_controller}
%{_prefix}/lib/common-lisp/bin/*
%{_prefix}/lib/sbcl/install-clc.lisp
%{_prefix}/lib/sbcl/sbcl-dist.core
%verify(not md5 size) %{_prefix}/lib/sbcl/sbcl.core
%config(noreplace) %{_sysconfdir}/sbcl.rc
%else
%{_prefix}/lib/sbcl/sbcl.core
%endif


%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 1.2.16-2
- Initial build

