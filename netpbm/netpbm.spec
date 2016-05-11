Summary:         A library for handling different graphics file formats
Name:            netpbm
Version:         10.71.02
Release:         2%{?dist}
# See copyright_summary for details
License:         BSD and GPLv2 and IJG and MIT and Public Domain
Group:           System Environment/Libraries
URL: http://netpbm.sourceforge.net/
# Source0 is prepared by
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced netpbm-%{version}
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide netpbm-%{version}/userguide
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/trunk/test netpbm-%{version}/test
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
# and removing the ppmtompeg code, due to patents ( rm -rf netpbm-%{version}/converter/ppm/ppmtompeg/ )
Source0:         netpbm-%{version}.tar.xz
Patch1:          netpbm-time.patch
Patch2:          netpbm-message.patch
Patch3:          netpbm-security-scripts.patch
Patch4:          netpbm-security-code.patch
Patch5:          netpbm-nodoc.patch
Patch6:          netpbm-gcc4.patch
Patch7:          netpbm-bmptopnm.patch
Patch8:          netpbm-CAN-2005-2471.patch
Patch9:          netpbm-xwdfix.patch
Patch11:         netpbm-multilib.patch
Patch13:         netpbm-glibc.patch
Patch15:         netpbm-docfix.patch
Patch16:         netpbm-ppmfadeusage.patch
Patch17:         netpbm-fiasco-overflow.patch
Patch20:         netpbm-noppmtompeg.patch
Patch21:         netpbm-cmuwtopbm.patch
Patch22:         netpbm-pamtojpeg2k.patch
Patch23:         netpbm-manfix.patch
Patch24:         netpbm-ppmtopict.patch
Patch26:         netpbm-werror.patch
Patch27:         netpbm-disable-pbmtog3.patch
Patch28:         netpbm-pnmtops.patch
Patch29:         netpbm-config.patch
BuildRequires:   libjpeg-devel, libpng-devel, libtiff-devel, flex
BuildRequires:   libX11-devel, python, jasper-devel, libxml2-devel
BuildRequires:   ghostscript
#BuildRequires:   ghostscript-core

%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package devel
Summary:         Development tools for programs which will use the netpbm libraries
Group:           Development/Libraries
Requires:        netpbm = %{version}-%{release}

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.  You'll also need
to have the netpbm package installed.

%package progs
Summary:         Tools for manipulating graphics files in netpbm supported formats
Group:           Applications/Multimedia
Requires:        ghostscript
Requires:        netpbm = %{version}-%{release}

%description progs
The netpbm-progs package contains a group of scripts for manipulating the
graphics files in formats which are supported by the netpbm libraries.  For
example, netpbm-progs includes the rasttopnm script, which will convert a
Sun rasterfile into a portable anymap.  Netpbm-progs contains many other
scripts for converting from one graphics file format to another.

If you need to use these conversion scripts, you should install
netpbm-progs.  You'll also need to install the netpbm package.

%package doc
Summary:         Documentation for tools manipulating graphics files in netpbm supported formats
Group:           Applications/Multimedia
Requires:        netpbm-progs = %{version}-%{release}

%description doc
The netpbm-doc package contains a documentation in HTML format for utilities
present in netpbm-progs package.

If you need to look into the HTML documentation, you should install
netpbm-doc.  You'll also need to install the netpbm-progs package.

%prep
%setup -q
%patch1 -p1 -b .time
%patch2 -p1 -b .message
%patch3 -p1 -b .security-scripts
%patch4 -p1 -b .security-code
%patch5 -p1 -b .nodoc
%patch6 -p1 -b .gcc4
%patch7 -p1 -b .bmptopnm
%patch8 -p1 -b .CAN-2005-2471
%patch9 -p1 -b .xwdfix
%patch11 -p1 -b .multilib
%patch13 -p1 -b .glibc
%patch15 -p1 -b .docfix
%patch16 -p1 -b .ppmfadeusage
%patch17 -p1 -b .fiasco-overflow
%patch20 -p1 -b .noppmtompeg
%patch21 -p1 -b .cmuwtopbmfix
%patch22 -p1 -b .pamtojpeg2kfix
%patch23 -p1 -b .manfix
%patch24 -p1 -b .ppmtopict
%patch26 -p1 -b .werror
%patch27 -p1 -b .disable-pbmtog3
%patch28 -p1 -b .pnmtops
%patch29 -p1 -b .config

sed -i 's/STRIPFLAG = -s/STRIPFLAG =/g' config.mk.in
rm -rf converter/other/jpeg2000/libjasper/
sed -i -e 's/^SUBDIRS = libjasper/SUBDIRS =/' converter/other/jpeg2000/Makefile

%build
./configure <<EOF



















EOF

TOP=`pwd`

make \
	CC="%{__cc}" \
	LDFLAGS="-L$TOP/pbm -L$TOP/pgm -L$TOP/pnm -L$TOP/ppm" \
	CFLAGS="$RPM_OPT_FLAGS -fPIC -flax-vector-conversions -fno-strict-aliasing" \
	LADD="-lm" \
	JPEGINC_DIR=%{_includedir} \
	PNGINC_DIR=%{_includedir} \
	TIFFINC_DIR=%{_includedir} \
	JPEGLIB_DIR=%{_libdir} \
	PNGLIB_DIR=%{_libdir} \
	TIFFLIB_DIR=%{_libdir} \
	LINUXSVGALIB="NONE" \
	X11LIB=%{_libdir}/libX11.so \
	XML2LIBS="NONE"

# prepare man files
cd userguide
# BZ 948531
rm -f ppmtompeg*
rm -f *.manual-pages
rm -f *.manfix
for i in *.html ; do
  ../buildtools/makeman ${i}
done
for i in 1 3 5 ; do
  mkdir -p man/man${i}
  mv *.${i} man/man${i}
done


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT
make package pkgdir=$RPM_BUILD_ROOT/usr LINUXSVGALIB="NONE" XML2LIBS="NONE"

# Ugly hack to have libs in correct dir on 64bit archs.
mkdir -p $RPM_BUILD_ROOT%{_libdir}
if [ "%{_libdir}" != "/usr/lib" ]; then
  mv $RPM_BUILD_ROOT/usr/lib/lib* $RPM_BUILD_ROOT%{_libdir}
fi

cp -af lib/libnetpbm.a $RPM_BUILD_ROOT%{_libdir}/libnetpbm.a
cp -l $RPM_BUILD_ROOT%{_libdir}/libnetpbm.so.?? $RPM_BUILD_ROOT%{_libdir}/libnetpbm.so

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv userguide/man $RPM_BUILD_ROOT%{_mandir}

# Get rid of the useless non-ascii character in pgmminkowski.1
sed -i 's/\xa0//' $RPM_BUILD_ROOT%{_mandir}/man1/pgmminkowski.1

# Don't ship man pages for non-existent binaries and bogus ones
for i in hpcdtoppm \
	 ppmsvgalib vidtoppm picttoppm \
	 directory error extendedopacity \
	 pam pbm pgm pnm ppm index libnetpbm_dir \
	 liberror ppmtotga; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man1/${i}.1
done
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/extendedopacity.5

mkdir -p $RPM_BUILD_ROOT%{_datadir}/netpbm
mv $RPM_BUILD_ROOT/usr/misc/*.map $RPM_BUILD_ROOT%{_datadir}/netpbm/
mv $RPM_BUILD_ROOT/usr/misc/rgb.txt $RPM_BUILD_ROOT%{_datadir}/netpbm/
rm -rf $RPM_BUILD_ROOT/usr/README
rm -rf $RPM_BUILD_ROOT/usr/VERSION
rm -rf $RPM_BUILD_ROOT/usr/link
rm -rf $RPM_BUILD_ROOT/usr/misc
rm -rf $RPM_BUILD_ROOT/usr/man
rm -rf $RPM_BUILD_ROOT/usr/pkginfo
rm -rf $RPM_BUILD_ROOT/usr/config_template
rm -rf $RPM_BUILD_ROOT/usr/pkgconfig_template

# Don't ship the static library
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.a

# remove/symlink/substitute obsolete utilities
pushd $RPM_BUILD_ROOT%{_bindir}
rm -f pgmtopbm pnmcomp
ln -s pamcomp pnmcomp
echo -e '#!/bin/sh\npamditherbw $@ | pamtopnm\n' > pgmtopbm
chmod 0755 pgmtopbm
popd

%check
pushd test
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export PBM_TESTPREFIX=$RPM_BUILD_ROOT%{_bindir}
export PBM_BINPREFIX=$RPM_BUILD_ROOT%{_bindir}
./Execute-Tests && exit 0
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc doc/COPYRIGHT.PATENT doc/HISTORY README
%license doc/GPL_LICENSE.txt
%{_libdir}/lib*.so*

%files devel
%dir %{_includedir}/netpbm
%{_includedir}/netpbm/*.h
%{_mandir}/man3/*

%files progs
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/netpbm/

%files doc
%doc userguide/*

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 10.71.02-2
- rebuilt for xen(libvirt)

