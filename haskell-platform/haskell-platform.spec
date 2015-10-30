#haskell-platform contains a lot of primitive haskell packages to form standard developmen environments.
#But every package may depend on other packages.
#So for first time build, you need install every packages in haskell-platform manually with below command:
#export LANG=en_US.utf8
#ghc --make -no-user-package-db Setup
#./Setup configure -p --prefix=/usr --libdir=/usr/lib '--libsubdir=$compiler/$pkgid' '--datasubdir=$pkgid' --enable-shared --global
#./Setup build
#sudo ./Setup copy -v
#sudo ./Setup register

#also need install packages(Source10 to Source17).

#after every package installed into system, we can build haskell-platform src.rpm.

#if we have old version of haskell-platform package installed, we can build it again.

%define debug_package %{nil}

Name: haskell-platform	
Version: 7.10.2
Release: 2
Summary: Standard Haskell distribution 	

License: BSD	
URL: http://www.haskell.org/platform/	
Source0: https://haskell.org/platform/download/7.10.2/haskell-platform-%{version}.tar.gz

Source1: cabal-install.sh

Source10: blaze-builder-0.4.0.1.tar.gz
Source11: extra-1.4.tar.gz
Source12: hastache-0.6.1.tar.gz
Source13: ieee754-0.7.6.tar.gz
Source14: js-flot-0.8.3.tar.gz
Source15: js-jquery-1.11.3.tar.gz
Source16: shake-0.15.4.tar.gz
Source17: utf8-string-1.tar.gz

BuildRequires: ghc, haskell-platform, haskell-platform-devel
BuildRequires: freeglut-devel
BuildRequires: gmp-devel
BuildRequires: libGLU-devel
BuildRequires: mesa-libGL-devel
BuildRequires: zlib-devel

Provides: alex, cabal-install, happy, hscolour, shake

%description
Haskell Platform is a suite of stable and well used Haskell libraries and tools.  
It provides a good starting environment for Haskell development.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

#add suppliments packages.
mkdir -p suppliments
tar zxf %{SOURCE10} -C suppliments 
tar zxf %{SOURCE11} -C suppliments 
tar zxf %{SOURCE12} -C suppliments 
tar zxf %{SOURCE13} -C suppliments 
tar zxf %{SOURCE14} -C suppliments 
tar zxf %{SOURCE15} -C suppliments 
tar zxf %{SOURCE16} -C suppliments 
tar zxf %{SOURCE17} -C suppliments 

%build
#build packages
pushd packages
for i in `cat ../etc/build.packages`
do
pushd $i
export LANG=en_US.utf8
ghc --make -no-user-package-db Setup
./Setup configure -p --prefix=%{_prefix} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-$i '--libsubdir=$compiler/$pkgid' '--datasubdir=$pkgid' --enable-shared --global
./Setup build
./Setup haddock --html --hyperlink-source --hoogle
popd
done
popd

#build suppliments
pushd suppliments
for i in `ls`
do
pushd $i
export LANG=en_US.utf8
ghc --make -no-user-package-db Setup
./Setup configure -p --prefix=%{_prefix} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-$i '--libsubdir=$compiler/$pkgid' '--datasubdir=$pkgid' --enable-shared --global
./Setup build
./Setup haddock --html --hyperlink-source --hoogle
popd
done
popd

%install
pushd packages
for i in `cat ../etc/build.packages`
do
pushd $i
./Setup copy --destdir=%{buildroot} -v
./Setup register --gen-pkg-config=$i.conf
GHC_VERSION=`ghc --numeric-version`
#some package only provides binaries and no libraries
if [ -f "$i.conf" ]; then
        install -D -m0644 $i.conf %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d/$i.conf
fi
popd
done
popd

#install suppliments package
pushd suppliments
for i in `ls`
do
pushd $i
./Setup copy --destdir=%{buildroot} -v
./Setup register --gen-pkg-config=$i.conf
GHC_VERSION=`ghc --numeric-version`
#some package only provides binaries and no libraries
if [ -f "$i.conf" ]; then
        install -D -m0644 $i.conf %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d/$i.conf
fi
popd
done
popd

#install cabal profile.d to setup user PATH.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

#install cabal bash completion
mkdir -p $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions
cp -p packages/cabal-install-*/bash-completion/cabal $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions


%post devel
/usr/bin/ghc-pkg recache --no-user-package-db || :
if [ -x /usr/share/doc/ghc/html/libraries/gen_contents_index ]; then
	cd /usr/share/doc/ghc/html/libraries
	./gen_contents_index >/dev/null 2>&1 ||:
fi ||:

%postun devel
/usr/bin/ghc-pkg recache --no-user-package-db || :

if [ -x /usr/share/doc/ghc/html/libraries/gen_contents_index ]; then
	cd /usr/share/doc/ghc/html/libraries
	./gen_contents_index >/dev/null 2>&1 ||:
fi ||:

%files
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/ghc-*/*/lib*.so
%{_datadir}/bash-completion/completions/*

%files devel
%{_libdir}/ghc-*
%{_docdir}/ghc-*
%{_docdir}/ghc
%{_datadir}/HUnit-*
%{_datadir}/alex-*
%{_datadir}/happy-*
%{_datadir}/hscolour-*
%{_datadir}/js-flot-*
%{_datadir}/js-jquery-*
%{_datadir}/shake-*

%exclude %{_libdir}/ghc-*/*/lib*.so

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 7.10.2-2
- Rebuild


