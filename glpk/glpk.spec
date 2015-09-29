Name:           glpk
Version:        4.55
Release:        4%{?dist}
Summary:        GNU Linear Programming Kit

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://www.gnu.org/software/glpk/glpk.html
Source0:        ftp://ftp.gnu.org/gnu/glpk/glpk-%{version}.tar.gz
# Un-bundle zlib (#1102855). Upstream won't accept; they want to be
# ANSI-compatible, and zlib makes POSIX assumptions.
Patch0:         glpk-4.55-unbundle-zlib.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gmp-devel
BuildRequires:  zlib-devel

%description
The GLPK (GNU Linear Programming Kit) package is intended for solving
large-scale linear programming (LP), mixed integer programming (MIP),
and other related problems. It is a set of routines written in ANSI C
and organized in the form of a callable library.

GLPK supports the GNU MathProg language, which is a subset of the AMPL
language.

The GLPK package includes the following main components:

 * Revised simplex method.
 * Primal-dual interior point method.
 * Branch-and-bound method.
 * Translator for GNU MathProg.
 * Application program interface (API).
 * Stand-alone LP/MIP solver. 

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation

%description    doc
Documentation subpackage for %{name}.


%package devel
Summary:        Development headers and files for GLPK
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The glpk-devel package contains libraries and headers for developing
applications which use GLPK (GNU Linear Programming Kit).


%package utils
Summary:        GLPK-related utilities and examples
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description utils
The glpk-utils package contains the standalone solver program glpsol
that uses GLPK (GNU Linear Programming Kit).


%package static
Summary:        Static version of GLPK libraries
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
The glpk-static package contains the statically linkable version of
the GLPK (GNU Linear Programming Kit) libraries.


%prep
%setup -q
%patch0 -p1 -b .system-zlib
rm -rf src/zlib

%build
export LIBS=-ldl

# Need to rebuild src/Makefile.in from src/Makefile.am
autoreconf -ifs

%configure --with-gmp
# Die die die, rpath.
sed -i -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i -e 's|LD_RUN_PATH||' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} libdir=$RPM_BUILD_ROOT%{_libdir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$RPM_BUILD_ROOT%{_libdir}"
make check
## Clean up directories that are included in docs
rm -Rf examples/{.deps,.libs,Makefile*,glpsol,glpsol.o} doc/*.tex

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING README
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS
%{_includedir}/glpk.h

%files utils
%defattr(-,root,root)
%{_bindir}/*

%files static
%defattr(-,root,root)
%{_libdir}/*.a
%exclude %{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc doc examples


%changelog
