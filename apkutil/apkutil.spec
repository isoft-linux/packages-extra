%define debug_package %{nil}

Summary: Android apk development/decompile/compile utilities 
Name: apkutil
Version: 4.4
Release: 6 
License: GPLv2+

#signapk source and testkey
Source0:  signapk.tar.gz

#wrapper script
Source2:  apkutil.sh

#pure java dalvikvm to test simple dex
Source3:  dalvikvm.tar.gz

#project template
Source4:  template.tar.gz


Source5:  elfhash-0.4.tar.gz
 
#droiddraw GUI Builder
Source10: https://droiddraw.googlecode.com/files/droiddraw-r1b22.tgz
Source11: androiddraw-signed.apk
#apktool
Source12: https://android-apktool.googlecode.com/files/apktool-install-linux-r05-ibot.tar.bz2
Source13: https://android-apktool.googlecode.com/files/apktool1.5.2.tar.bz2

#dex2jar
Source14: https://dex2jar.googlecode.com/files/dex2jar-0.0.9.15.zip

#smali/baksmali
Source15: https://smali.googlecode.com/files/smali-2.0b6.jar
Source16: https://smali.googlecode.com/files/baksmali-2.0b6.jar

#android api16 and dx from android sourcetree
Source17: android-sdk-4.1.2.tar.xz


#soot.jar include dava decompiler
Source19: http://www.sable.mcgill.ca/software/soot-2.5.0.jar


#vim smali syntax
Source30:  filetype.vim
Source31:  smali.vim

#smali HelloWorld example
Source40:  example.tar.gz

#this patch let binutils objcopy can rehash .hash section when we want to change a jni function namespace.

Patch0:    binutils-objcopy-rehash.patch    

BuildRequires: openjdk
Requires: openjdk
Requires: android-utils

%description
Android apk development/decompile/re-compile utilities.

include:
    signapk
    apktool
    smali/baksmali
    dx

%prep
%setup -c -a0 -a3 -a5

%build
pushd elfhash-0.4
make
popd


pushd signapk
make
popd

pushd dalvikvm
make
popd
   

%install
pushd elfhash-0.4
make install DESTDIR=$RPM_BUILD_ROOT
popd

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil
#wrapper script
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/apkutil
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf %{_datadir}/apkutil/apkutil.sh $RPM_BUILD_ROOT/usr/bin/apkutil 

#project template
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/apkutil

#signapk
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/signapk
pushd signapk
    install -m 0644 signapk.jar $RPM_BUILD_ROOT/%{_datadir}/apkutil/signapk
    install -m 0644 testkey.pk8 $RPM_BUILD_ROOT/%{_datadir}/apkutil/signapk
    install -m 0644 testkey.x509.pem $RPM_BUILD_ROOT/%{_datadir}/apkutil/signapk
popd

#dalvikvm
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/dalvikvm
pushd dalvikvm
install -m 0644 dalvikvm.jar $RPM_BUILD_ROOT/%{_datadir}/apkutil/dalvikvm
popd

#smali/baksmali
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/smali
install -m 0644 %{SOURCE15} $RPM_BUILD_ROOT/%{_datadir}/apkutil/smali/smali.jar
install -m 0644 %{SOURCE16} $RPM_BUILD_ROOT/%{_datadir}/apkutil/smali/baksmali.jar


#droiddraw
if [ "`tar --help | grep -- --strip-components 2> /dev/null`" ]; then
    TARSTRIP=--strip-components
elif [ "`tar --help | grep bsdtar 2> /dev/null`" ]; then
    TARSTRIP=--strip-components
else
    TARSTRIP=--strip-path
fi

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/droiddraw
tar ${TARSTRIP}=1 -xf %{SOURCE10} -C $RPM_BUILD_ROOT/%{_datadir}/apkutil/droiddraw
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/apkutil/droiddraw

#apktool
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/apktool
tar ${TARSTRIP}=1 -xf %{SOURCE12} -C $RPM_BUILD_ROOT/%{_datadir}/apkutil/apktool
tar ${TARSTRIP}=1 -xf %{SOURCE13} -C $RPM_BUILD_ROOT/%{_datadir}/apkutil/apktool
rm -rf $RPM_BUILD_ROOT/%{_datadir}/apkutil/apktool/aapt

#dex2jar
unzip %{SOURCE14} -d $RPM_BUILD_ROOT/%{_datadir}/apkutil
mv $RPM_BUILD_ROOT/%{_datadir}/apkutil/dex2jar-* $RPM_BUILD_ROOT/%{_datadir}/apkutil/dex2jar

#android sdk
tar xf %{SOURCE17} -C $RPM_BUILD_ROOT/%{_datadir}/apkutil

#soot/ava
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/apkutil/soot
install -m 0644 %{SOURCE19} $RPM_BUILD_ROOT/%{_datadir}/apkutil/soot/soot.jar

#example
tar zxf %{SOURCE40} -C $RPM_BUILD_ROOT/%{_datadir}/apkutil



mkdir -p $RPM_BUILD_ROOT/usr/share/vim/vimfiles/ftdetect
install -m 0644 %{SOURCE30} $RPM_BUILD_ROOT/usr/share/vim/vimfiles/ftdetect/smali.vim
mkdir -p $RPM_BUILD_ROOT/usr/share/vim/vimfiles/syntax
install -m 0644 %{SOURCE31} $RPM_BUILD_ROOT/usr/share/vim/vimfiles/syntax/smali.vim


%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
/usr/bin/*
/usr/share/apkutil
/usr/share//vim/vimfiles/ftdetect/*
/usr/share//vim/vimfiles/syntax/*

