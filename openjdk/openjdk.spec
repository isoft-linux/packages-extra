%define update_version 60 
%define build_number 24

%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

Name: openjdk	
Version: 8u%{update_version}b%{build_number}
Release: 1
Summary: Oracle OpenJDK via IcedTea
License: ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL: http://openjdk.java.net/

#http://hg.openjdk.java.net/jdk8u/jdk8u60/archive/jdk8u60-b24.tar.bz2
Source0: jdk8u%{update_version}-jdk8u%{update_version}-b%{build_number}.tar.bz2

Source1: corba-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source2: hotspot-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source3: jaxp-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source4: jaxws-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source5: langtools-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source6: jdk-jdk8u%{update_version}-b%{build_number}.tar.bz2
Source7: nashorn-jdk8u%{update_version}-b%{build_number}.tar.bz2

#above sources downloaded by this script, NOTE: change version numbers when update.
Source10: download-openjdk-sources.sh 

Source100:  openjdk.sh


Patch0:   adlc-parser.patch
#this patch is important, otherwise icedteaWeb not work.
Patch1:   applet-hole.patch
Patch2:   autoconf-select.diff
Patch3:   compare-pointer-with-literal.patch
Patch4:   atk-wrapper-security.patch
Patch5:   workaround_expand_exec_shield_cs_limit.diff
Patch6:   multiple-pkcs11-library-init.patch
Patch7:   java-1.8.0-openjdk-accessible-toolkit.patch

Patch10:  disable-doclint-by-default.diff
Patch11:  dnd-files.patch
Patch12:  dont-strip-images.diff
Patch13:  hotspot-disable-werror.diff
Patch14:  hotspot-set-compiler.diff
Patch15:  icedtea-4953367.patch
Patch16:  ld-symbolic-functions-default.diff
Patch17:  libpcsclite-dlopen.diff
Patch18:  make4-compatibility.diff
Patch19:  nonreparenting-wm.diff
Patch20:  zero-missing-headers.diff

#from tuxjdk
#https://code.google.com/p/tuxjdk/
#this patch is rebased with 8u60b24.
Patch40: add-fontconfig-support.diff 
Patch41: lcd-hrgb-by-default.diff
Patch42: jdk-freetypeScaler-crash.diff

#this patch is force to enable on the spot input method style for fcitx.
#Cursor follow issue still exists!!!!!!!!!!!
#currently, there is no way to fix it in awt_InputMethod.c
#By Cjacker
Patch60: force-to-on-the-spot-xim-style.patch

#try to fix cursor follow issue in SWING/AWT, swing should works. awt still had some problem about cursor position calculate.
#!!!!!!!!!!!!!!Please do not apply this time, since it's will cause deadlock.
Patch61: try-to-fix-xim-spotlocation.patch

BuildRequires: gcc
BuildRequires: findutils tar zip gawk pkgconfig util-linux
BuildRequires: ca-certificates libxslt zip
BuildRequires: autoconf automake 
BuildRequires: nss-devel cups-devel 
BuildRequires: libjpeg-turbo-devel giflib-devel libpng-devel lcms2-devel 
BuildRequires: libXt-devel libXp-devel libXtst-devel libXinerama-devel libXrender-devel 
BuildRequires: libattr-devel zlib-devel alsa-lib-devel freetype-devel fontconfig-devel krb5-devel
BuildRequires: gtk2-devel 

BuildRequires: alsa-lib-devel
BuildRequires: cpio unzip which zip
BuildRequires: cups-devel
BuildRequires: libX11-devel

BuildRequires: openjdk


#disable autorequires and provides
AutoReqProv: no
#at least
Requires: libgcc, libstdc++

#for trust
Requires: p11-kit-trust

Provides: java
Provides: java-devel


%description
%{summary}

%prep
%setup -q -n jdk8u%{update_version}-jdk8u%{update_version}-b%{build_number} -a1 -a2 -a3 -a4 -a5 -a6 -a7
mv corba-jdk8u%{update_version}-b%{build_number} corba
mv hotspot-jdk8u%{update_version}-b%{build_number} hotspot
mv jaxp-jdk8u%{update_version}-b%{build_number} jaxp
mv jaxws-jdk8u%{update_version}-b%{build_number} jaxws
mv langtools-jdk8u%{update_version}-b%{build_number} langtools
mv jdk-jdk8u%{update_version}-b%{build_number} jdk
mv nashorn-jdk8u%{update_version}-b%{build_number} nashorn

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

%patch40 -p1
%patch41 -p1
%patch42 -p1

%patch60 -p1


%build
#ensure use gcc/g++
export CC=gcc
export CXX=g++

#Modern Java installations do not need JAVA_HOME 
unset JAVA_HOME

sh ./configure \
   --with-milestone="isoft" \
   --with-update-version=%{update_version} \
   --with-build-number=b%{build_number} \
   --with-debug-level=release \
   --enable-unlimited-crypto  \
   --with-zlib=system \
   --with-giflib=system \
   --with-x \
   --with-cups \
   --with-alsa \
   --with-jobs=`/usr/bin/getconf _NPROCESSORS_ONLN`

make DISABLE_HOTSPOT_OS_VERSION_CHECK=ok all

find build/*/images/j2sdk-image -iname \*.diz -delete


%install
IMG_PATH=`find . -name j2sdk-image -type d`

mkdir -p $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8

cp -RT $IMG_PATH $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8


#fix perms if needed, use ||: to avoid failed.
pushd $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8
find . -perm 600|xargs chmod 644 ||:
popd

install -Dm0755 %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/openjdk.sh


# Install cacerts symlink.
rm -f $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8/jre/lib/security/cacerts
pushd $RPM_BUILD_ROOT%{_libdir}/jvm/openjdk8/jre/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_libdir}/jvm/openjdk8/jre/lib/security)
    ln -sf $RELATIVE/cacerts .
popd

%post

%files
%{_sysconfdir}/profile.d/openjdk.sh
%dir %{_libdir}/jvm/openjdk8
%{_libdir}/jvm/openjdk8/*

%changelog
* Thu Aug 06 2015 Cjacker <cjacker@foxmail.com>
- update openjdk to 8u60b24.

