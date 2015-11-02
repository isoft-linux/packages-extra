Name:		clisp
Summary:	ANSI Common Lisp implementation
Version:	2.49
Release:	2%{?dist}

License:	GPLv2
URL:		http://www.clisp.org/
Source0:	%{name}-%{version}.tar.bz2   
# http://sourceforge.net/tracker/?func=detail&aid=3529615&group_id=1355&atid=301355
Patch1:         %{name}-arm.patch
# Linux-specific fixes.  Sent upstream 25 Jul 2012.
Patch4:         %{name}-linux.patch
# Adapt to GCC 5.x
Patch5:         %{name}-gcc5.patch


BuildRequires:	dbus-devel
BuildRequires:	ffcall
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	ghostscript
BuildRequires:	groff
BuildRequires:	gtk2-devel
BuildRequires:	libXaw-devel
BuildRequires:	libXft-devel
BuildRequires:	libdb-devel
BuildRequires:	libglade2-devel
BuildRequires:	libsigsegv-devel
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel

ExcludeArch:	ppc64 aarch64

# clisp contains a copy of gnulib, which has been granted a bundling exception:
Provides:	bundled(gnulib)

%description
ANSI Common Lisp is a high-level, general-purpose programming
language.  GNU CLISP is a Common Lisp implementation by Bruno Haible
of Karlsruhe University and Michael Stoll of Munich University, both
in Germany.  It mostly supports the Lisp described in the ANSI Common
Lisp standard.  It runs on most Unix workstations (GNU/Linux, FreeBSD,
NetBSD, OpenBSD, Solaris, Tru64, HP-UX, BeOS, NeXTstep, IRIX, AIX and
others) and on other systems (Windows NT/2000/XP, Windows 95/98/ME)
and needs only 4 MiB of RAM.

It is Free Software and may be distributed under the terms of GNU GPL,
while it is possible to distribute commercial proprietary applications
compiled with GNU CLISP.

The user interface comes in English, German, French, Spanish, Dutch,
Russian and Danish, and can be changed at run time.  GNU CLISP
includes an interpreter, a compiler, a debugger, CLOS, MOP, a foreign
language interface, sockets, i18n, fast bignums and more.  An X11
interface is available through CLX, Garnet, CLUE/CLIO.  GNU CLISP runs
Maxima, ACL2 and many other Common Lisp packages.


%package devel
Summary:	Development files for CLISP
Provides:	%{name}-static = %{version}-%{release} 
Requires:	%{name}%{?_isa} = %{version}-%{release}, automake

%description devel
Files necessary for linking CLISP programs.

%prep
%setup -q
%patch1 -p0
%patch4 -p0
%patch5 -p0

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--docdir=%{_docdir}/clisp-%{version} \
	--with-readline \
	--with-ffcall \
	src
cd src
ulimit -s unlimited
./makemake --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir} --infodir=%{_infodir} --docdir=%{_docdir}/clisp-%{version} --with-readline --with-ffcall --with-dynamic-ffi > Makefile
make
sed -i 's,http://www.lisp.org/HyperSpec/,http://www.lispworks.com/reference/HyperSpec/,g' config.lisp
make

%install
pushd src
make install DESTDIR=%{buildroot}
popd

#remove duplicated docs.
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp-link.html
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp-link.pdf
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp-link.ps
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp.html
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp.pdf
rm -rf %{buildroot}%{_docdir}/clisp-%{version}/clisp.ps

#match _pkgdocdir
mv %{buildroot}%{_docdir}/clisp-%{version} %{buildroot}%{_docdir}/%{name}

%find_lang %{name}
%find_lang %{name}low
cat %{name}low.lang >> %{name}.lang

%check
pushd src
ulimit -s unlimited
make check
popd

%files -f %{name}.lang
%{_pkgdocdir}
%{_bindir}/clisp
%{_mandir}/man1/clisp.1.gz
%dir %{_libdir}/clisp-%{version}/
%{_libdir}/clisp-%{version}/base/
%{_libdir}/clisp-%{version}/data/
%{_libdir}/clisp-%{version}/dynmod/
%{_datadir}/emacs/site-lisp/*
%{_datadir}/vim/vimfiles/after/syntax/*


%files devel
%{_bindir}/clisp-link
%{_mandir}/man1/clisp-link.1.gz
%{_datadir}/aclocal/clisp.m4
%{_libdir}/clisp-%{version}/build-aux/
%{_libdir}/clisp-%{version}/base/*.a
%{_libdir}/clisp-%{version}/base/*.o
%{_libdir}/clisp-%{version}/base/*.h
%{_libdir}/clisp-%{version}/base/makevars
%{_libdir}/clisp-%{version}/linkkit/

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 2.49-2
- Initial build

