#haskell-platform contains a lot of primitive haskell packages to form standard developmen environments.
#But pkgs may depend on other pkgs, then it's very difficult to bootstrap haskell-platform as whole single pkg.
#A lot of dists choose to install every haskell module seperately, but it's hard to maintain and we do not like that.

#we still insist build haskell-platform as single package, for resolve dependency issue, we choose cabal sandbox.

#1, build and install all pkgs into sandbox.
#2, re-configure every pkg global and rebuild it.

%define debug_package %{nil}

%define alex_ver 3.1.4
%define happy_ver 1.19.5

Name: haskell-platform	
Version: 7.10.3
Release: 3
Summary: Standard Haskell distribution 	

License: BSD
URL: http://www.haskell.org/platform/	
Source0: https://haskell.org/platform/download/7.10.2/haskell-platform-%{version}.tar.gz

Source10: blaze-builder-0.4.0.1.tar.gz
Source11: extra-1.4.2.tar.gz
Source12: hastache-0.6.1.tar.gz
Source13: ieee754-0.7.6.tar.gz
Source14: js-flot-0.8.3.tar.gz
Source15: js-jquery-1.11.3.tar.gz
Source16: shake-0.15.4.tar.gz
Source17: utf8-string-1.0.1.1.tar.gz
Source18: doctest-0.10.1.tar.gz
Source19: ghc-paths-0.1.0.9.tar.gz

BuildRequires: ghc, cabal, hscolour
BuildRequires: alex, happy 
BuildRequires: freeglut-devel
BuildRequires: gmp-devel
BuildRequires: libGLU-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: zlib-devel

Provides: shake = 0.15.4-%{release}
Provides: doctest = 0.10.1-%{release}

Requires: ghc cabal hscolour alex happy

%description
Haskell Platform is a suite of stable and well used Haskell libraries and tools.

It provides a good starting environment for Haskell development.

This package also include essential packages not included in official haskell-platform release, such as:
blaze-builder
extra
hastache
ieee754
js-flot
js-jquery
shake
utf8-string
doctest
ghc-paths

%package -n alex 
Version: %{alex_ver}
URL: http://www.haskell.org/alex
Summary: Alex is a tool for generating lexical analysers in Haskell

%description -n alex 
lex is a tool for generating lexical analysers in Haskell.

It takes a description of tokens based on regular expressions
and generates a Haskell module containing code for scanning text efficiently.

It is similar to the tool lex or flex for C/C++.

%package -n happy
Version: %{happy_ver}
URL: http://www.haskell.org/happy
Summary: Happy is a parser generator for Haskell

%description -n happy 
Happy is a parser generator for Haskell. 

Given a grammar specification in BNF, Happy generates Haskell code to parse the grammar. 

Happy works in a similar way to the yacc tool for C.

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
tar zxf %{SOURCE18} -C suppliments 
tar zxf %{SOURCE19} -C suppliments 

%build
export SANDBOX=`pwd`/.cabal-sandbox
export DIST=`pwd`/cabal-build
rm -rf $DIST

#enable document build
#enable profile build
cat >cabal.config <<EOF
documentation: True
library-profiling: True
EOF

#setup PATH to sandbox 
export PATH=`pwd`/.cabal-sandbox/usr/bin:$PATH

#init sandbox
cabal sandbox init

#modify sandbox config file to match global ghc dir layout.
sed -i 's%^  bindir: .*%  bindir: $prefix/usr/bin%' cabal.sandbox.config
sed -i 's%^  libdir: .*%  libdir: $prefix/usr/lib%' cabal.sandbox.config
sed -i 's%^  libsubdir: .*%  libsubdir: $compiler/$pkgid%' cabal.sandbox.config
sed -i 's%^  libexecdir: .*%  libexecdir: $prefix/usr/libexec%' cabal.sandbox.config
sed -i 's%^  datadir: .*%  datadir: $prefix/usr/share%' cabal.sandbox.config
sed -i 's%^  datasubdir: .*%  datasubdir: $pkgid%' cabal.sandbox.config
sed -i 's%^  docdir: .*%  docdir: $datadir/doc/ghc-$pkgid%' cabal.sandbox.config
sed -i 's%^  htmldir: .*%  htmldir: $prefix/usr/share/doc/ghc/html/libraries/$pkgid%' cabal.sandbox.config


#add suppliments libraries to sandbox
for i in `find ./suppliments -maxdepth 1 -type d`
do
if [ ! x$i = x"./suppliments" ]; then
cabal sandbox add-source `pwd`/$i
fi
done

#add packages to sandbox
for i in `cat ./etc/build.packages`
do
cabal sandbox add-source `pwd`/packages/$i
done

#build to sandbox.
#install every pkg to sandbox.
#since we add all sources to sandbox, it may be installed as required by other package already, this's ok.
#cabal install will ignore installed pkgs.

for i in packages/*
do
pkgname=`basename $i`
cabal install $pkgname
done

for i in suppliments/*
do
pkgname=`basename $i`
cabal install $pkgname
done

#Sandbox build finished.
#NOW re-configure every components global.

pushd packages
for i in *
do
 pushd $i
 #for find local installed pkgs.
 ln -s ../../cabal.sandbox.config .
 cabal clean
 cabal configure -p --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
 cabal build
 cabal haddock --html --hyperlink-source --hoogle
 popd
done
popd

pushd suppliments
for i in * 
do
 pushd $i
 #for find local installed pkgs.
 ln -s ../../cabal.sandbox.config .
 cabal clean
 cabal configure -p --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
 cabal build
 cabal haddock --html --hyperlink-source --hoogle
 popd
done
popd

%install
mkdir -p %{buildroot}
pushd suppliments
for i in * 
do
 pushd $i
 cabal copy --destdir=%{buildroot}
# cabal register --gen-pkg-config=$i.conf
# GHC_VERSION=`ghc --numeric-version`
# #some package only provides binaries and no libraries
# if [ -f "$i.conf" ]; then
#         install -D -m0644 $i.conf %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d/$i.conf
# fi
 popd
done
popd

pushd packages
for i in *
do
 pushd $i
 cabal copy --destdir=%{buildroot}
# cabal register --gen-pkg-config=$i.conf
# GHC_VERSION=`ghc --numeric-version`
# #some package only provides binaries and no libraries
# if [ -f "$i.conf" ]; then
#         install -D -m0644 $i.conf %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d/$i.conf
# fi
 popd
done
popd


#intall pkg conf
GHC_VERSION=`ghc --numeric-version`
mkdir -p %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d
cp .cabal-sandbox/*-packages.conf.d/*.conf %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d/

#fixup PATH in pkg config file, it contains sandbox PATH.
pushd %{buildroot}%{_libdir}/ghc-$GHC_VERSION/package.conf.d
for i in *.conf
do
sed -i 's|: /.*sandbox/|: /|g' $i
done

#they are in seperated pkgs.
rm -rf %{buildroot}%{_bindir}/cabal
rm -rf %{buildroot}%{_bindir}/HsColour
rm -rf %{buildroot}%{_datadir}/hscolour-*
rm -rf %{buildroot}%{_docdir}/ghc-hscolour-*
rm -rf %{buildroot}%{_docdir}/ghc-cabal-*

#document index generated in sandbox
rm -rf %{buildroot}%{_docdir}/*-ghc-$GHC_VERSION

%posttrans
/usr/bin/ghc-pkg recache --no-user-package-db || :
if [ -x /usr/share/doc/ghc/html/libraries/gen_contents_index ]; then
	cd /usr/share/doc/ghc/html/libraries
	./gen_contents_index >/dev/null 2>&1 ||:
fi ||:

%postun
/usr/bin/ghc-pkg recache --no-user-package-db || :

if [ -x /usr/share/doc/ghc/html/libraries/gen_contents_index ]; then
	cd /usr/share/doc/ghc/html/libraries
	./gen_contents_index >/dev/null 2>&1 ||:
fi ||:

%files
%{_bindir}/mkReadme
%{_bindir}/shake
%{_bindir}/doctest
%{_libdir}/ghc-*/*
%{_datadir}/HUnit-*
%{_datadir}/js-flot-*
%{_datadir}/js-jquery-*
%{_datadir}/shake-*
%{_docdir}/ghc/html/*
#pkg docs,license file.
%{_docdir}/ghc-*

%files -n alex
%{_bindir}/alex
%{_datadir}/alex-*

%files -n happy
%{_bindir}/happy
%{_datadir}/happy-*

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 7.10.3-3
- Rebuild, sep alex/happay pkgs

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 7.10.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 7.10.2-2
- Rebuild


