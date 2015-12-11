%define debug_package %{nil}

Name: leksah 
Version: 0.15.1.4
Release: 3
Summary: Haskell IDE written in Haskel

License: GPL
URL: http://www.leksah.org 
Source0: https://hackage.haskell.org/package/leksah-%{version}/leksah-%{version}.tar.gz
#1,download leksah, untar
#cabal install regex-tdfa-text --ghc-options=-XFlexibleContexts
#cabal install gtk2hs-buildtools
#cabal install leksah
#cabal install --only-dependencies
#it will download all dependencies and install it.
#tar all download dependencies here.
Source1: %{name}-hackage.tar.gz

Patch0: leksah-default-browser-to-xdg-open.patch
Patch1: leksah-about-dialog-logo.patch

BuildRequires: ghc haskell-platform
BuildRequires: webkitgtk-devel cairo-devel glib2-devel gtk2-devel gtksourceview-devel
BuildRequires: cairo-gobject-devel atk-devel gdk-pixbuf2-devel libsoup-devel zlib-devel
BuildRequires: chrpath

Requires: ghc haskell-platform alex happy hscolour cabal
Requires: xdg-utils

%description
%{summary}

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

#extract all sources.
pushd %{name}-hackage
for i in *.tar.gz
do
tar zxf $i
done
popd

rm -rf %{name}-hackage/*.tar.gz


%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

export SANDBOX=`pwd`/.cabal-sandbox
export DIST=`pwd`/cabal-build
rm -rf $DIST


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

export PATH=`pwd`/.cabal-sandbox/usr/bin:$PATH


#add all local library to sandbox
for i in %{name}-hackage/*
do
  cabal sandbox add-source `pwd`/$i
done

#start build.
cabal clean
cabal install regex-tdfa-text --ghc-options=-XFlexibleContexts
cabal install gtk2hs-buildtools

for i in %{name}-hackage/*
do
pkgname=`basename $i`
cabal install $pkgname
done

pushd %{name}-hackage/vcswrapper-0.1.2
ln -s ../../cabal.sandbox.config .
cabal clean
cabal configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build
popd

pushd %{name}-hackage/vcsgui-0.1.3.0
ln -s ../../cabal.sandbox.config .
cabal clean
cabal configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build
popd

pushd %{name}-hackage/leksah-server-0.15.0.9
ln -s ../../cabal.sandbox.config .
cabal clean
cabal configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build
popd

#configure and install leksah
cabal clean
cabal configure --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build


%install
pushd %{name}-hackage/vcswrapper-0.1.2
cabal copy --destdir=%{buildroot}
popd

pushd %{name}-hackage/vcsgui-0.1.3.0
cabal copy --destdir=%{buildroot}
popd

pushd %{name}-hackage/leksah-server-0.15.0.9
cabal copy --destdir=%{buildroot}
popd

cabal copy --destdir=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications
install -m0644 linux/applications/leksah.desktop %{buildroot}%{_datadir}/applications/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -m0644 linux/icons/hicolor/48x48/apps/leksah_48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/leksah.png

#unneeded libraries
rm -rf %{buildroot}%{_libdir}/ghc-*

#unneeded docs
rm -rf %{buildroot}%{_docdir}/ghc-leksah-*

#remove rpath
chrpath -d %{buildroot}%{_bindir}/vcswrapper
chrpath -d %{buildroot}%{_bindir}/leksahtrue
chrpath -d %{buildroot}%{_bindir}/leksah-server
chrpath -d %{buildroot}%{_bindir}/leksah
chrpath -d %{buildroot}%{_bindir}/bewleksah
chrpath -d %{buildroot}%{_bindir}/vcsgui
chrpath -d %{buildroot}%{_bindir}/vcsgui-askpass
chrpath -d %{buildroot}%{_bindir}/leksahecho

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/leksah
%{_bindir}/leksahecho
%{_bindir}/leksah-server
%{_bindir}/leksahtrue
%{_bindir}/vcswrapper
%{_bindir}/vcsgui-askpass
%{_bindir}/vcsgui
%{_bindir}/bewleksah

%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/48x48/apps/leksah.png

%{_datadir}/leksah-server-0.*
%{_datadir}/leksah-0.*
%{_datadir}/vcsgui-0.*
%{_datadir}/vcswrapper-0.*

%changelog
* Thu Dec 10 2015 Cjacker <cjacker@foxmail.com> - 0.15.1.4-3
- Rebuild

* Thu Dec 10 2015 Cjacker <cjacker@foxmail.com> - 0.15.1.4-2
- Initial build


