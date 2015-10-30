Name:           pstoedit
Version:        3.70
Release:        4
Summary:        Translates PostScript and PDF graphics into other vector formats

License:        GPLv2+
URL:            http://www.pstoedit.net/
Source0:        http://downloads.sourceforge.net/pstoedit/pstoedit-%{version}.tar.gz

Requires:       ghostscript
BuildRequires:  gd-devel
BuildRequires:  libpng-devel
BuildRequires:  dos2unix
BuildRequires:  ghostscript
BuildRequires:  plotutils-devel
%ifnarch ia64
BuildRequires:  libEMF-devel
%endif

%description
Pstoedit converts PostScript and PDF files to various vector graphic
formats. The resulting files can be edited or imported into various
drawing packages. Pstoedit comes with a large set of integrated format
drivers


%package devel
Summary:        Headers for developing programs that will use %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libpng-devel

%description devel
This package contains the header files needed for developing %{name}
applications


%prep
%setup -q

dos2unix doc/*.htm doc/readme.txt


%build
# Buildling without ImageMagick support, to work around bug 507035
%configure --disable-static --with-emf --without-swf --without-magick

# http://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 doc/pstoedit.1 $RPM_BUILD_ROOT%{_mandir}/man1/
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc copying doc/readme.txt doc/pstoedit.htm
%{_datadir}/pstoedit
%{_mandir}/man1/*
%{_bindir}/pstoedit
%{_libdir}/*.so.*
%{_libdir}/pstoedit


%files devel
%doc doc/changelog.htm
%{_includedir}/pstoedit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.70-4
- Rebuild

