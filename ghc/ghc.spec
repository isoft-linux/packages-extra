#build ghc need ghc.
#for first build, you need to download the binary release of ghc from official site
#./configure --prefix=/opt/ghc;make install.

#for first build.
#hscolour is not available, since it need ghc to build, you can comment out the buildrequires.

Name: ghc	
Version: 7.10.3
Release: 2
Summary: Glasgow Haskell Compiler	

License: BSD and HaskellReport
URL: http://www.haskell.org/ghc	
Source0: http://downloads.haskell.org/~ghc/7.10.2/ghc-%{version}-src.tar.xz
Source1: http://downloads.haskell.org/~ghc/7.10.2/ghc-%{version}-testsuite.tar.xz

Source4: ghc-doc-index

BuildRequires: ghc
BuildRequires: gcc binutils
BuildRequires: hscolour
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: libxslt, docbook-style-xsl
BuildRequires: python
BuildRequires: autoconf, automake
BuildRequires: libxml2-devel
BuildRequires: sed tar patch perl findutils coreutils grep
# BuildRequires: llvm
Provides: haddock

%description
GHC is a state-of-the-art, open source, compiler and interactive environment
for the functional language Haskell. Highlights:

- GHC supports the entire Haskell 2010 language plus various extensions.
- GHC has particularly good support for concurrency and parallelism,
  including support for Software Transactional Memory (STM).
- GHC generates fast code, particularly for concurrent programs
  (check the results on the "Computer Language Benchmarks Game").
- GHC works on several platforms including Windows, Mac, Linux,
  most varieties of Unix, and several different processor architectures.
- GHC has extensive optimisation capabilities,
  including inter-module optimisation.
- GHC compiles Haskell code either directly to native code or using LLVM
  as a back-end. GHC can also generate C code as an intermediate target for
  porting to new platforms. The interactive environment compiles Haskell to
  bytecode, and supports execution of mixed bytecode/compiled programs.
- Profiling is supported, both by time/allocation and heap profiling.
- GHC comes with core libraries, and thousands more are available on Hackage.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version} -b1

%build
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --with-gcc=%{_bindir}/gcc

export LANG=en_US.utf8
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}


mkdir -p %{buildroot}%{_localstatedir}/lib/ghc
install -p --mode=0755 %SOURCE4 %{buildroot}%{_bindir}/ghc-doc-index

%posttrans
%{_bindir}/ghc-pkg recache --no-user-package-db || :

%files
%{_bindir}/ghc*
%{_bindir}/haddock*
%{_bindir}/hp2ps
%{_bindir}/hpc
%{_bindir}/hsc2hs
%{_bindir}/runghc*
%{_bindir}/runhaskell
%{_localstatedir}/lib/ghc
%{_libdir}/ghc-*
%{_mandir}/man1/ghc.*

%{_docdir}/ghc

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 7.10.3-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 7.10.2-2
- Rebuild

* Fri Jul 31 2015 Cjacker <cjacker@foxmail.com>
- first build.
