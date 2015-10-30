Summary: A complete ODBC driver manager for Linux
Name: unixODBC
Version: 2.3.4
Release: 2%{?dist}
URL: http://www.unixODBC.org/
# Programs are GPL, libraries are LGPL, except News Server library is GPL.
License: GPLv2+ and LGPLv2+

Source: http://www.unixODBC.org/%{name}-%{version}.tar.gz
Source1: odbcinst.ini
Source4: conffile.h
Source5: README.dist

Patch6: export-symbols.patch
Patch8: so-version-bump.patch
Patch9: keep-typedefs.patch

Conflicts: iodbc

BuildRequires: automake autoconf libtool libtool-ltdl-devel bison flex
BuildRequires: readline-devel

%description
Install unixODBC if you want to access databases through ODBC.
You will also need the mysql-connector-odbc package if you want to access
a MySQL database, and/or the postgresql-odbc package for PostgreSQL.

%package devel
Summary: Development files for programs which will use the unixODBC library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The unixODBC package can be used to access databases through ODBC
drivers. If you want to develop programs that will access data through
ODBC, you need to install this package.

%prep
%setup -q
%patch6 -p1
%patch8 -p1 -b .soname-bump
%patch9 -p1

chmod 0644 Drivers/MiniSQL/*.c
chmod 0644 Drivers/nn/*.c
chmod 0644 Drivers/template/*.c
chmod 0644 doc/ProgrammerManual/Tutorial/*.html
chmod 0644 doc/lst/*
chmod 0644 include/odbcinst.h

# Blow away the embedded libtool and replace with build system's libtool.
# (We will use the installed libtool anyway, but this makes sure they match.)
rm -rf config.guess config.sub install-sh ltmain.sh libltdl depcomp missing
# this hack is so we can build with either libtool 2.2 or 1.5
libtoolize --install --copy || libtoolize --copy

%build

aclocal
automake --add-missing
autoheader
autoconf

# unixODBC 2.2.14 is not aliasing-safe
CFLAGS="%{optflags} -fno-strict-aliasing"
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

%configure \
    --with-gnu-ld=yes \
    --enable-threads=yes \
    --enable-drivers=yes \
    --enable-driverc=yes \
    --enable-ltdllib

# Get rid of the rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make all

%install
make DESTDIR=$RPM_BUILD_ROOT install
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

# add some explanatory documentation
cp %{SOURCE5} README.dist

# remove obsolete Postgres drivers from the package (but not the setup code)
rm -f $RPM_BUILD_ROOT%{_libdir}/libodbcpsql.so*

# copy text driver documentation into main doc directory
# currently disabled because upstream no longer includes text driver
# mkdir -p doc/Drivers/txt
# cp -pr Drivers/txt/doc/* doc/Drivers/txt

# don't want to install doc Makefiles as docs
find doc -name 'Makefile*' | xargs rm

# we do not want to ship static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libltdl.*
rm -rf $RPM_BUILD_ROOT%{_datadir}/libtool

# initialize lists of .so files
find $RPM_BUILD_ROOT%{_libdir} -name "*.so.*" | sed "s|^$RPM_BUILD_ROOT||" > base-so-list
find $RPM_BUILD_ROOT%{_libdir} -name "*.so"   | sed "s|^$RPM_BUILD_ROOT||" > devel-so-list

# move these to main package, they're often dlopened...
for lib in libodbc.so libodbcinst.so libodbcpsqlS.so libodbcmyS.so
do
    echo "%{_libdir}/$lib" >> base-so-list
    grep -v "/$lib$" devel-so-list > devel-so-list.x
    mv -f devel-so-list.x devel-so-list
done

%files -f base-so-list
%doc README COPYING AUTHORS ChangeLog NEWS doc
%doc README.dist
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/odbcinst
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_bindir}/slencheck
%{_mandir}/man*/*

%files devel -f devel-so-list
%{_includedir}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 2.3.4-2
- Initial build

