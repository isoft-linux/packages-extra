%define enable_japanese 1

Summary: Converts LaTeX documents to HTML
Name: latex2html
Version: 2012
Release: 7
License: GPLv2+
Group: Applications/Publishing
URL: http://www.latex2html.org/
# main latex2html source
Source0: http://mirrors.ctan.org/support/latex2html/%{name}-%{version}.tgz
Source1: cfgcache.pm
Source2: %{name}-manpages.tar.gz
# support for Japanese
Source3: http://takeno.iee.niit.ac.jp/~shige/TeX/latex2html/current/data/l2h-2K8-jp20081220.tar.gz
Patch0: latex2html-2K.1beta-tabularx.patch
Patch1: teTeX-l2h-config.patch
Patch3: latex2html-2K.1beta-DB.patch
Patch4: latex2html-2002-2-1-SHLIB.patch
Patch5: latex2html-2002-2-1-gsfont.patch
Patch6: latex2html-2002.2.1-grayimg.patch
Requires:  netpbm-progs
#Requires: tex(latex), tex(dvips), tex(url.sty), netpbm-progs
BuildRequires: perl >= 5.003, ghostscript >= 4.03, netpbm-progs >= 9.21
#BuildRequires: perl >= 5.003, ghostscript >= 4.03, netpbm-progs >= 9.21, tex(latex)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
LATEX2HTML is a converter written in Perl that converts LATEX
documents to HTML. This way e.g. scientific papers - primarily typeset
for printing - can be put on the Web for online viewing.

LATEX2HTML does also a good job in rapid web site deployment. These
pages are generated from a single LATEX source.

%prep
%setup -q -n %{name}-%{version} -c -a 0

pushd %{name}-%{version}
# patch latex2html to support tabularx environments better
%patch0 -p1 -b .tabularx

# Patch from Oliver Paukstadt <oliver.paukstadt@millenux.com>
%patch1 -p2 -b .config

# Fix latex2html not to use DB_File
%patch3 -p2 -b .db_file

# fix SHLIBDIR
%patch4 -p1 -b .shlib

# don't require the font directory to be ended with PATH/fonts
%patch5 -p1 -b .gsfont

# remove all platforms we don't need
for i in Dos Mac OS2 Win32; do
  rm -f L2hos/${i}.pm
done
rm -rf cweb2html
rm -f readme.hthtml
popd

%if %{enable_japanese}
cp -a %{name}-%{version} %{name}-%{version}JA
pushd %{name}-%{version}JA
tar fxz %{SOURCE3}
popd
%endif

pushd %{name}-%{version}
# don't generate gray images as output from latex2html
# it's patched here to let the .jp2 patch be cleanly applied
%patch6 -p1 -b .grayimg
popd

%build
pushd %{name}-%{version}
cp %{SOURCE1} cfgcache.pm
tar fxz %{SOURCE2}

./configure	--program-prefix=%{?_program_prefix} \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix} \
		--bindir=%{_bindir} \
		--sbindir=%{_sbindir} \
		--sysconfdir=%{_sysconfdir} \
		--datadir=%{_datadir} \
		--includedir=%{_includedir} \
		--libdir=%{_datadir}/latex2html \
		--libexecdir=%{_libexecdir} \
		--localstatedir=%{_localstatedir} \
		--sharedstatedir=%{_sharedstatedir} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--shlibdir=%{_datadir}/latex2html \
		--with-texpath=%{_datadir}/texmf/tex/latex/html

perl -pi -e"s,/usr/(share/)?lib,%{_datadir}," cfgcache.pm
make
popd

%if %{enable_japanese}
pushd %{name}-%{version}JA
sed s/latex2html/jlatex2html/g < %{SOURCE1} > cfgcache.pm
perl -pi -e"s,/usr/bin/dvips,/usr/bin/pdvips," cfgcache.pm
perl -pi -e"s,/usr/bin/latex,/usr/bin/platex," cfgcache.pm

./configure	--program-prefix=%{?_program_prefix} \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix} \
		--bindir=%{_bindir} \
		--sbindir=%{_sbindir} \
		--sysconfdir=%{_sysconfdir} \
		--datadir=%{_datadir} \
		--includedir=%{_includedir} \
		--libdir=%{_datadir}/jlatex2html \
		--libexecdir=%{_libexecdir} \
		--localstatedir=%{_localstatedir} \
		--sharedstatedir=%{_sharedstatedir} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--shlibdir=%{_datadir}/jlatex2html \
		--with-texpath=%{_datadir}/texmf/tex/latex/html

perl -pi -e"s,/usr/(share/)?lib,%{_datadir},;
	    s,%{_datadir}/latex2html,%{_datadir}/jlatex2html," cfgcache.pm
make
perl -pi -e"s,\\\${dd}pstoimg,\\\${dd}jpstoimg, ;
	    s,\\\${dd}texexpand,\\\${dd}jtexexpand," l2hconf.pm

for i in latex2html pstoimg texexpand ; do
	mv ${i} j${i}
done
popd
%endif

%install
rm -rf %{buildroot}

pushd %{name}-%{version}
perl -pi -e"s,%{_prefix},%{buildroot}%{_prefix}," cfgcache.pm
perl -pi -e"s,/.*\\\${dd}texexpand,%{_bindir}/texexpand,;
	    s,/.*\\\${dd}pstoimg,%{_bindir}/pstoimg,;
	    s,/.*\\\${dd}*icons,\\\${LATEX2HTMLDIR}/icons,;
	    s,/.*\\\${dd}rgb.txt,\\\${LATEX2HTMLDIR}/styles/rgb.txt,;
	    s,/.*\\\${dd}styles\\\${dd}crayola.txt,\\\${LATEX2HTMLDIR}/styles/crayola.txt," latex2html
perl -pi -e"s,%{buildroot},," l2hconf.pm

make install
rm -f %{buildroot}%{_datadir}/latex2html/versions/table.pl.orig
rm -rf %{buildroot}%{_datadir}/latex2html/docs/
rm -rf %{buildroot}%{_datadir}/latex2html/example/
perl -pi -e"s,%{buildroot},," %{buildroot}%{_datadir}/latex2html/cfgcache.pm
perl -pi -e"s,%{buildroot},," %{buildroot}%{_bindir}/pstoimg
perl -pi -e"s,%{buildroot},," %{buildroot}%{_bindir}/texexpand
perl -pi -e"s,%{buildroot},," cfgcache.pm
perl -pi -e"s,$cfg{'GS_LIB'} = q'';,$cfg{'GS_LIB'} = q'%{_datadir}/ghostscript/`ghostscript --version`';," cfgcache.pm
install -m0644 *.pm %{buildroot}%{_datadir}/latex2html
chmod +x %{buildroot}%{_datadir}/latex2html/makeseg/makeseg %{buildroot}%{_datadir}/latex2html/makemap

# install man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -m0644 *.1 %{buildroot}%{_mandir}/man1
popd

%if %{enable_japanese}
pushd %{name}-%{version}JA
perl -pi -e"s,%{_prefix},%{buildroot}%{_prefix}," cfgcache.pm
perl -pi -e"s,latex2html pstoimg texexpand,jlatex2html jpstoimg jtexexpand," config/install.pl
perl -pi -e"s,/.*\\\${dd}texexpand,%{_bindir}/jtexexpand,;
	    s,/.*\\\${dd}pstoimg,%{_bindir}/jpstoimg,;
	    s,/.*\\\${dd}icons,\\\${LATEX2HTMLDIR}/icons,;
	    s,/.*\\\${dd}styles\\\${dd}rgb.txt,\\\${LATEX2HTMLDIR}/styles/rgb.txt,;
	    s,/.*\\\${dd}styles\\\${dd}crayola.txt,\\\${LATEX2HTMLDIR}/styles/crayola.txt," jlatex2html
perl -pi -e"s,%{buildroot},," l2hconf.pm

make install
rm -f %{buildroot}%{_datadir}/jlatex2html/versions/table.pl.orig
rm -rf %{buildroot}%{_datadir}/jlatex2html/docs/
rm -rf %{buildroot}%{_datadir}/jlatex2html/example/
perl -pi -e"s,%{buildroot},," %{buildroot}%{_datadir}/jlatex2html/cfgcache.pm
perl -pi -e"s,%{buildroot},," %{buildroot}%{_bindir}/jpstoimg
perl -pi -e"s,%{buildroot},," %{buildroot}%{_bindir}/jtexexpand
perl -pi -e"s,%{buildroot},," cfgcache.pm
perl -pi -e"s,$cfg{'GS_LIB'} = q'';,$cfg{'GS_LIB'} = q'%{_datadir}/ghostscript/`ghostscript --version`';," cfgcache.pm
install -m0644 *.pm %{buildroot}%{_datadir}/jlatex2html
chmod +x %{buildroot}%{_datadir}/jlatex2html/makeseg/makeseg %{buildroot}%{_datadir}/jlatex2html/makemap
popd
%endif

for f in cweb2html/cweb2html makeseg/makeseg makemap ; do
	perl -pi -e "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/latex2html/$f
%if %{enable_japanese}
	perl -pi -e "s,/usr/local/bin/perl,/usr/bin/perl," %{buildroot}%{_datadir}/jlatex2html/$f
%endif
done

# do not clash with texlive, prefer url.sty from texlive instead
rm -f %{buildroot}%{_datadir}/texmf/tex/latex/html/url.sty

%clean
rm -rf %{buildroot}

%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :

%files
%defattr(-,root,root,-)
%doc latex2html-%{version}/{LICENSE,LICENSE.orig,README,FAQ,BUGS,docs,example}
%{_bindir}/latex2html
%{_bindir}/pstoimg
%{_bindir}/texexpand
%dir %{_datadir}/latex2html
%{_datadir}/latex2html/*
%dir %{_datadir}/texmf/tex/latex/html
%{_datadir}/texmf/tex/latex/html/*

%if %{enable_japanese}
%{_bindir}/jlatex2html
%{_bindir}/jpstoimg
%{_bindir}/jtexexpand
%dir %{_datadir}/jlatex2html
%{_datadir}/jlatex2html/*
%endif

%{_mandir}/man1/latex2html.*
%{_mandir}/man1/texexpand.*
%{_mandir}/man1/pstoimg.*

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 2012-7
- rebuilt for xen

