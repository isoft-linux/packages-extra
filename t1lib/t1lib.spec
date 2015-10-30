Name:           t1lib
Version:        5.1.2
Release:        18%{?dist}

Summary:        PostScript Type 1 font rasterizer

License:        LGPLv2+
URL:            ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.lsm
Source0:        ftp://sunsite.unc.edu/pub/Linux/libs/graphics/t1lib-%{version}.tar.gz
Patch0:         http://ftp.de.debian.org/debian/pool/main/t/t1lib/t1lib_5.1.2-3.diff.gz
Patch1:         t1lib-5.1.2-segf.patch
# Fixes CVE-2010-2642, CVE-2011-0433
Patch2:         t1lib-5.1.2-afm-fix.patch
# Fixes CVE-2011-0764, CVE-2011-1552, CVE-2011-1553, CVE-2011-1554
Patch3:         t1lib-5.1.2-type1-inv-rw-fix.patch
# Add aarch64 support
Patch4:         t1lib-5.1.2-aarch64.patch
Patch5:         t1lib-5.1.2-format-security.patch

BuildRequires:  libXaw-devel

Requires(post): coreutils, findutils

%description
T1lib is a rasterizer library for Adobe Type 1 Fonts. It supports
rotation and transformation, kerning underlining and antialiasing. It
does not depend on X11, but does provides some special functions for
X11.

AFM-files can be generated from Type 1 font files and font subsetting
is possible.

%package        apps
Summary:        t1lib demo applications
Requires:       %{name} = %{version}-%{release}

%description    apps
Sample applications using t1lib

%package        devel
Summary:        Header files and development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and development files for %{name}.

%package        static
Summary:        Static libraries for %{name}
Requires:       %{name}-devel = %{version}-%{release}

%description    static
This package contains static libraries for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .segf
%patch2 -p1 -b .afm-fix
%patch3 -p1 -b .type1-inv-rw-fix
%patch4 -p1 -b .aarch64
%patch5 -p1 -b .format-security

# use debian patches directly instead of duplicating them
#patch -p1 < debian/patches/segfault.diff -b -z .segf
patch -p1 < debian/patches/no-config.diff
patch -p1 < debian/patches/no-docs.diff
patch -p1 < debian/patches/lib-cleanup.diff

iconv -f latin1 -t utf8 < Changes > Changes.utf8
touch -r Changes Changes.utf8
mv Changes.utf8 Changes


%build
%configure

# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} without_doc
touch -r lib/t1lib/t1lib.h.in lib/t1lib.h
touch -r lib/t1lib/t1libx.h lib/t1libx.h
ln README.t1lib-%{version} README
sed -e 's;/usr/share/X11/fonts;%{_datadir}/X11/fonts;' \
  -e 's;/usr/share/fonts/type1;%{_datadir}/fonts %{_datadir}/texmf/fonts;' \
  -e 's;/etc/t1lib/;%{_datadir}/t1lib/;' \
 debian/t1libconfig > t1libconfig
touch -r README.t1lib-%{version} t1libconfig

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/libt1*.la
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libt1*.so.*

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
install -p -m 644 debian/man/FontDatabase.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install -p -m 644 debian/man/t1libconfig.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -p -m 644 debian/man/type1afm.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 644 debian/man/xglyph.1 $RPM_BUILD_ROOT%{_mandir}/man1/
touch -r README.t1lib-%{version} $RPM_BUILD_ROOT%{_mandir}/man?/*.*

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -p -m 755 t1libconfig $RPM_BUILD_ROOT%{_sbindir}/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/t1lib/
touch $RPM_BUILD_ROOT%{_datadir}/t1lib/{FontDatabase,t1lib.config}

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
%{_sbindir}/t1libconfig --force > /dev/null

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Changes LGPL LICENSE README
%dir %{_datadir}/t1lib
%ghost %verify(not size mtime md5) %{_datadir}/t1lib/t1lib.config
%ghost %verify(not size mtime md5) %{_datadir}/t1lib/FontDatabase
%{_libdir}/libt1.so.*
%{_libdir}/libt1x.so.*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/t1libconfig

%files apps
%defattr(-,root,root,-)
%{_bindir}/type1afm
%{_bindir}/xglyph
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/t1lib_doc.pdf
%{_includedir}/t1lib*.h
%{_libdir}/libt1.so
%{_libdir}/libt1x.so

%files static
%defattr(-,root,root,-)
%{_libdir}/libt1.a
%{_libdir}/libt1x.a


%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 5.1.2-18
- Initial build

