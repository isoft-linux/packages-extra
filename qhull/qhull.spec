Summary: General dimension convex hull programs
Name: qhull
Version: 2003.1
Release: 26%{?dist}
License: Qhull
Group: System Environment/Libraries
Source0: http://www.qhull.org/download/qhull-%{version}.tar.gz
Patch0: qhull-2003.1-alias.patch
Patch1: http://www.qhull.org/download/qhull-2003.1-qh_gethash.patch
# Add pkgconfig support
Patch2: qhull-2003.1-pkgconfig.patch
# Misc. fixes related to 64bit compliance
Patch3: qhull-2003.1-64bit.patch
# Update config.{guess,sub} for *-aarch64 (RHBZ #926411)
Patch4: qhull-2003.1-config.patch
Patch5: qhull-2003.1-format-security.patch

URL: http://www.qhull.org

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%package devel
Group: Development/Libraries
Summary: Development files for qhull
Requires: %{name} = %{version}-%{release}

%description devel
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i -e "s,\"../html/,\"html/,g" src/*.htm

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

sed -e 's|@prefix@|%{_prefix}|' \
  -e 's|@exec_prefix@|%{_exec_prefix}|' \
  -e 's|@includedir@|%{_includedir}|' \
  -e 's|@libdir@|%{_libdir}|' \
  -e 's|@VERSION@|%{version}|' \
  qhull.pc.in > qhull.pc

%install
make DESTDIR=$RPM_BUILD_ROOT \
  docdir=%{_pkgdocdir} install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

install -m644 -D qhull.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/qhull.pc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_pkgdocdir}
%_bindir/*
%_libdir/*.so.*
%_mandir/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/qhull.pc
%{_includedir}/*


%changelog
