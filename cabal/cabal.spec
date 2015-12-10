#we use cabal sandbox to avoid pollut system.
%define debug_package %{nil}

Name: cabal 
Version: 1.22.6.0
Release: 3
Summary: Haskell Package Manager

License: BSD3
URL: http://www.haskell.org/cabal/ 
Source0: https://hackage.haskell.org/package/cabal-install-%{version}/cabal-install-%{version}.tar.gz 

#for bootstrap, use bootstrap.sh, it will download and installed all dependecy pkgs, build and install them in ~/.cabal
Source1: cabal-hackages.tar.gz

Source10: cabal-install.sh

BuildRequires: ghc gcc binutils cabal	
BuildRequires: zlib-devel gmp-devel

Provides: cabal-install = %{version}-%{release}

%description
Simplifies the process of managing Haskell software by
automating the fetching, configuration, compilation and installation of Haskell libraries and programs.

%prep
%setup -q -n cabal-install-%{version} -a1
#extract all sources.
pushd cabal-hackages
for i in *.tar.gz
do
tar zxf $i
done
popd

%build
export SANDBOX=`pwd`/.cabal-sandbox
export DIST=`pwd`/cabal-build
rm -rf $DIST
#init sandbox
cabal sandbox init

#add all local library to sandbox
for i in `find ./cabal-hackages -maxdepth 1 -type d`
do
if [ ! x$i = x"./cabal-hackages" ]; then
cabal sandbox add-source `pwd`/$i
fi
done

#start build.
cabal clean
cabal install

#all dependencies is in sandbox now, re-configure cabal as global.
cabal clean
cabal configure -p --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build

%install
mkdir -p %{buildroot}
cabal copy --destdir=%{buildroot}

#install cabal profile.d to setup user PATH.
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d

#install cabal bash completion
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
cp -p bash-completion/cabal %{buildroot}%{_datadir}/bash-completion/completions

%files
%{_bindir}/cabal
%{_sysconfdir}/profile.d/*.sh
%{_datadir}/bash-completion/completions/cabal
%{_docdir}/ghc-cabal-*

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.22.6.0-3
- Rebuild

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.22.6.0-2
- Initial build, use cabal sandbox to avoid pollut system.


