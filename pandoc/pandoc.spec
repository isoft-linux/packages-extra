#We use cabal sandbox to build pandoc to avoid network online required.

%define debug_package %{nil}

Name: pandoc
Version: 1.15.2.1
Release: 2
Summary: Converting from one markup format to another 

License: GPL 
URL: http://www.pandoc.org
#do not use source from github, it miss some submodules.
Source0: http://hackage.haskell.org/package/pandoc-%{version}/pandoc-%{version}.tar.gz

#pandoc dependencies, all packages is taken from ~/.cabal of manually build.
Source1: hackages.tar.gz

BuildRequires: ghc, haskell-platform, cabal, chrpath

%description
Pandoc is a Haskell library for converting from one markup
format to another, and a command-line tool that uses
this library. It can read markdown and (subsets of) HTML,
reStructuredText, LaTeX, DocBook, MediaWiki markup, TWiki
markup, Haddock markup, OPML, Emacs Org-Mode, txt2tags,
Word Docx, ODT, and Textile, and it can write
Markdown, reStructuredText, XHTML, HTML 5, LaTeX,
ConTeXt, DocBook, OPML, OpenDocument, ODT,
Word docx, RTF, MediaWiki, DokuWiki, Textile, groff man
pages, plain text, Emacs Org-Mode, AsciiDoc, Haddock markup,
EPUB (v2 and v3), FictionBook2, InDesign ICML, and several
kinds of HTML/javascript slide shows (S5, Slidy, Slideous,
DZSlides, reveal.js).

Pandoc extends standard markdown syntax with footnotes,
embedded LaTeX, definition lists, tables, and other
features. A compatibility mode is provided for those
who need a drop-in replacement for Markdown.pl.

In contrast to existing tools for converting markdown
to HTML, which use regex substitutions, pandoc has
a modular design: it consists of a set of readers,
which parse text in a given format and produce a native
representation of the document, and a set of writers,
which convert this native representation into a target
format. Thus, adding an input or output format requires
only adding a reader or writer.


%prep
%setup -q -a1

#extract all sources.
pushd hackages
for i in `ls *.tar.gz`
do
tar zxf $i
done
popd

#avoid this conflict.
sed -i 's#ghc-prim >= 0.2 && < 0.4#ghc-prim#g' ./hackages/deepseq-generics-0.1.1.2/deepseq-generics.cabal

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

export SANDBOX=`pwd`/.cabal-sandbox
export DIST=`pwd`/pandoc-build
rm -rf $DIST

#init sandbox
cabal sandbox init

#add all local library to sandbox
for i in `find ./hackages -maxdepth 1 -type d`
do
if [ ! x$i = x"./hackages" ]; then
cabal sandbox add-source `pwd`/$i
fi
done

#build and install hsb2hs locally.
export PATH=`pwd`/.cabal-sandbox/bin:$PATH
cabal install hsb2hs

#build pandoc
cabal clean
cabal install --force --reinstall --flags="embed_data_files make-pandoc-man-pages" . pandoc-citeproc


cabal clean
cabal configure --flags="embed_data_files make-pandoc-man-pages" --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global
cabal build

pushd hackages/pandoc-citeproc-0.8.0.1
ln ../../cabal.sandbox.config .
cabal clean

cabal configure --flags="embed_data_files make-pandoc-man-pages" --prefix=%{_prefix} --bindir=%{_bindir} --libdir=%{_libdir} --htmldir=%{_docdir}/ghc/html/libraries/$i --docdir=%{_docdir}/ghc-%{name}-%{version} '--libsubdir=$compiler/$pkgid' --datadir=%{_datadir} --libexecdir=%{_libexecdir} '--datasubdir=$pkgid' --enable-shared --global

cabal build
popd

%install
cabal copy --destdir=%{buildroot}

pushd hackages/pandoc-citeproc-0.8.0.1
cabal copy --destdir=%{buildroot}
popd

rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_docdir}
#no need to keep data files, already embeded in ELF.
rm -rf %{buildroot}%{_datadir}/pandoc-*

chrpath -d %{buildroot}%{_bindir}/pandoc
chrpath -d %{buildroot}%{_bindir}/pandoc-citeproc
 
%files
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 1.15.2.1-2
- Update

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 1.15.1.1-2
- Initial build


