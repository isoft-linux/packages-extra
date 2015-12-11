#We use cabal sandbox to build to avoid pollut system.

#And this pkg only provide hscolour command to used by ghc build, hscolour library will provided in haskell platform.

%define debug_package %{nil}

Name: hscolour
Version: 1.23
Release: 4 
Summary: Small Haskell script to colourise Haskell code
License: GPL 
URL: https://hackage.haskell.org/package/hscolour 
Source0: https://hackage.haskell.org/package/hscolour-%{version}/hscolour-%{version}.tar.gz

BuildRequires: ghc cabal

BuildRequires: gcc binutils gmp-devel

BuildRequires: chrpath

%description
hscolour is a small Haskell script to colourise Haskell code. It currently has six output formats: ANSI terminal codes (optionally XTerm-256colour codes), HTML 3.2 with font tags, HTML 4.01 with CSS, HTML 4.01 with CSS and mouseover annotations, XHTML 1.0 with inline CSS styling, LaTeX, and mIRC chat codes.

%prep
%setup -q

%build
cabal configure -p --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global

cabal build

%install
mkdir -p %{buildroot}
cabal copy --destdir=%{buildroot}

chrpath -d %{buildroot}%{_bindir}/HsColour

rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_docdir}

%files
%{_bindir}/*
%{_datadir}/hscolour-*

%changelog
* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 1.23-4
- Strip rpath

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.23-3
- Rebuild

* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 1.23-2
- Initial build



