Summary: Windows MetaFile Library
Name: libwmf
Version: 0.2.8.4
Release: 49%{?dist}
#libwmf is under the LGPLv2+, however...
#1. The tarball contains an old version of the urw-fonts under GPL+.
#   Those fonts are not installed
#2. The header of the command-line wmf2plot utility places it under the GPLv2+.
#   wmf2plot is neither built or install
License: LGPLv2+ and GPLv2+ and GPL+
Source: http://downloads.sourceforge.net/wvware/%{name}-%{version}.tar.gz
URL: http://wvware.sourceforge.net/libwmf.html
#Upstream is uncontactable for some time now, which is a real pity esp.
#wrt CVE-2006-3376/CVE-2009-1364
#Don't install out of date documentation
Patch0:  libwmf-0.2.8.3-nodocs.patch
#Allow use of system install fonts intead of libwmf bundled ones
Patch1:  libwmf-0.2.8.3-relocatablefonts.patch
#Set a fallback font of Times for text if a .wmf file don't set any
Patch2:  libwmf-0.2.8.4-fallbackfont.patch
#Strip unnecessary extra library dependencies
Patch3:  libwmf-0.2.8.4-deps.patch
#convert libwmf-config to a pkg-config to avoid multilib conflicts
Patch4:  libwmf-0.2.8.4-multiarchdevel.patch
#CVE-2006-3376 Integer overflow in player.c
Patch5:  libwmf-0.2.8.4-intoverflow.patch
#Don't export the modified embedded GD library symbols, to avoid conflicts with
#the external one
Patch6:  libwmf-0.2.8.4-reducesymbols.patch
#CVE-2009-1364, Use-after-free vulnerability in the modified embedded GD
#library
Patch7:  libwmf-0.2.8.4-useafterfree.patch
# adapt to standalone gdk-pixbuf
Patch8:  libwmf-0.2.8.4-pixbufloaderdir.patch
# CVE-2007-0455
Patch9:  libwmf-0.2.8.4-CVE-2007-0455.patch
# CVE-2007-3472
Patch10: libwmf-0.2.8.4-CVE-2007-3472.patch
# CVE-2007-3473
Patch11: libwmf-0.2.8.4-CVE-2007-3473.patch
# CVE-2006-2906 affects GIFs, which is not implemented here
# CVE-2006-4484 affects GIFs, which is not implemented here
# CVE-2007-3474 affects GIFs, which is not implemented here
# CVE-2007-3475 affects GIFs, which is not implemented here
# CVE-2007-3476 affects GIFs, which is not implemented here
# CVE-2007-3477
Patch12: libwmf-0.2.8.4-CVE-2007-3477.patch
# CVE-2007-3478 affects shared ttf files across threads, which is not implemented here
# CVE-2007-2756
Patch13: libwmf-0.2.8.4-CVE-2007-2756.patch
# CAN-2004-0941
Patch14: libwmf-0.2.8.4-CAN-2004-0941.patch
# CVE-2009-3546
Patch15: libwmf-0.2.8.4-CVE-2009-3546.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=925929
Patch16: libwmf-aarch64.patch
# CVE-2015-0848+CVE-2015-4588
Patch17: libwmf-0.2.8.4-CVE-2015-0848+CVE-2015-4588.patch
# CVE-2015-4695
Patch18: libwmf-0.2.8.4-CVE-2015-4695.patch
# CVE-2015-4696
Patch19: libwmf-0.2.8.4-CVE-2015-4696.patch

Requires: urw-fonts
Requires: %{name}-lite = %{version}-%{release}

# for file triggers
Requires: gdk-pixbuf2%{?_isa} >= 2.31.5-2.fc24

BuildRequires: gtk2-devel, libtool, libxml2-devel, libpng-devel
BuildRequires: libjpeg-devel, libXt-devel, libX11-devel, dos2unix, libtool

%description
A library for reading and converting Windows MetaFile vector graphics (WMF).

%package lite
Summary: Windows Metafile parser library

%description lite
A library for parsing Windows MetaFile vector graphics (WMF).

%package devel
Summary: Support files necessary to compile applications with libwmf
Requires: libwmf = %{version}-%{release}
Requires: gtk2-devel, libxml2-devel, libjpeg-devel

%description devel
Libraries, headers, and support files necessary to compile applications 
using libwmf.

%prep
%setup -q
%patch0  -p1 -b .nodocs
%patch1  -p1 -b .relocatablefonts
%patch2  -p1 -b .fallbackfont
%patch3  -p1 -b .deps
%patch4  -p1 -b .multiarchdevel
%patch5  -p1 -b .intoverflow
%patch6  -p1 -b .reducesymbols.patch
%patch7  -p1 -b .useafterfree.patch
%patch8  -p1 -b .pixbufloaderdir
%patch9  -p1 -b .CVE-2007-0455
%patch10 -p1 -b .CVE-2007-3472
%patch11 -p1 -b .CVE-2007-3473
%patch12 -p1 -b .CVE-2007-3477
%patch13 -p1 -b .CVE-2007-2756
%patch14 -p1 -b .CAN-2004-0941
%patch15 -p1 -b .CVE-2009-3546
%patch16 -p1 -b .aarch64
%patch17 -p1 -b .CVE-2015-0848+CVE-2015-4588
%patch18 -p1 -b .CVE-2015-4695
%patch19 -p1 -b .CVE-2015-4696
f=README ; iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f

%build
rm configure.ac
ln -s patches/acconfig.h acconfig.h
autoreconf -i -f
%configure --with-libxml2 --disable-static --disable-dependency-tracking
make %{?_smp_mflags}
dos2unix doc/caolan/*.html

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_includedir}/libwmf/gd
find doc -name "Makefile*" -exec rm {} \;

#we're carrying around duplicate fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*afm
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*pfb
sed -i $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/fontmap -e 's#libwmf/fonts#fonts/default/Type1#g'

%post -p /sbin/ldconfig

%post lite -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun lite -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libwmf-*.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_bindir}/wmf2svg
%{_bindir}/wmf2gd
%{_bindir}/wmf2eps
%{_bindir}/wmf2fig
%{_bindir}/wmf2x
%{_bindir}/libwmf-fontmap
%{_datadir}/libwmf/

%files lite
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libwmflite-*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html
%doc doc/*.png
%doc doc/*.gif
%doc doc/html
%doc doc/caolan
%{_libdir}/*.so
%{_libdir}/pkgconfig/libwmf.pc
%{_includedir}/libwmf
%{_bindir}/libwmf-config


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.8.4-49
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.2.8.4-48
- Initial build. 

