%ifarch alpha ia64 x86_64 ppc64 ppc64le sparc64 s390x aarch64
%define bits	64
%else
%define bits	32
%endif

Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 0.95.19
Release: 2%{?dist}
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/

#  download the latest git source for 0.91 branch from
#   http://gitorious.org/freetds/freetds/archive-tarball/Branch-0_91
#  then
#   mv freetds-freetds-Branch-0_91.tar.gz freetds-%{version}-%{git_commit}.tar.gz
#Source0: freetds-%{version}-%{git_commit}.tar.gz

Source0: ftp://ftp.freetds.org/pub/freetds/stable/freetds-%{version}.tar.bz2
Source1: freetds-tds_sysdep_public.h

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: unixODBC-devel, readline-devel, gnutls-devel, krb5-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtool
BuildRequires: doxygen, docbook-style-dsssl


%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.


%package doc
Summary: Development documentation for %{name}
Group: Documentation
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.


%prep 
%setup -q

#  correct perl path
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl

chmod -x samples/*.sh


%build 

[ -f configure ] || NOCONFIGURE=yes ./autogen.sh

%configure \
	--disable-dependency-tracking \
	--disable-rpath \
	--disable-static \
	--with-tdsver="4.2" \
	--with-unixodbc="%{_prefix}" \
	--enable-msdblib \
	--enable-sybase-compat \
	--with-gnutls \
	--enable-krb5

#  disable-rpath in configure does not work...
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_RIE|' libtool


make %{?_smp_mflags} DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | fgrep html/docbook.dsl`"

 
%install 
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
chmod -x $RPM_BUILD_ROOT%{_sysconfdir}/*

mv -f $RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public.h \
	$RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public_%{bits}.h
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/tds_sysdep_public.h

rm -f samples/Makefile* samples/*.in samples/README

mv -f samples/unixodbc.freetds.driver.template \
	samples/unixodbc.freetds.driver.template-%{bits}

#  deinstall it for our own way...
mv -f $RPM_BUILD_ROOT%{_docdir}/%{name} docdir
find docdir -type f -print0 | xargs -0 chmod -x


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean 
rm -rf $RPM_BUILD_ROOT
 

%files 
%defattr(-, root, root, -) 
%{_bindir}/*
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/*.conf
%doc AUTHORS BUGS COPYING* NEWS README TODO doc/*.html
%doc docdir/userguide docdir/images
%{_mandir}/*/*

 
%files devel 
%defattr (-, root, root, -) 
%doc samples
%{_libdir}/*.so
%{_includedir}/*


%files doc
%defattr (-, root, root, -) 
%doc docdir/reference
 

%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 0.95.19-2
- Initial build

