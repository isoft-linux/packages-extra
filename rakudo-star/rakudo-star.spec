#
# disables the check: brp-java-repack-jars
# needed that the following error do not happen:
#  Unhandled exception: java.lang.RuntimeException: Bytecode jar contains
#  unexpected file META-INF/
#     in  (src/stage2/gen/NQP.nqp)
#
%define __jar_repack %{nil}


# disable empty nqp-debug package
%define debug_package %{nil}


%global year 2015
%global month 09


Name:           rakudo-star
Version:        0.0.%{year}.%{month}
Release:        1%{?dist}
Summary:        Rakudo, Perl6-modules and documentation
License:        Artistic 2.0
Group:          Development/Languages
URL:            http://www.rakudo.org/

Source0:        http://rakudo.org/downloads/star/rakudo-star-%{year}.%{month}.tar.gz
# sources for desktop files are added here
Source1:        http://github.com/downloads/gerd/desktop-files/rakudo.desk.tar.gz

BuildRequires:  perl(ExtUtils::Command)
BuildRequires:  perl(Test::Harness)

BuildRequires:  readline-devel

BuildRequires:  nqp >= 0.0.%{year}.%{month}
Requires:  nqp >= 0.0.%{year}.%{month}


# Build with MoarVM
BuildRequires:  nqp >= 0.0.%{year}.%{month}
Requires:  nqp >= 0.0.%{year}.%{month}
BuildRequires:  moarvm-devel
BuildRequires:  libuv-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  libtommath-devel
BuildRequires:  sha-devel

# currently disable the building of the jvm subpackage
%define build_jvm_exec 0

# Build with JVM
%if %{build_jvm_exec}
BuildRequires:  jpackage-utils
BuildRequires:  java
BuildRequires:  java-devel

Requires:       java

BuildRequires:  nqp-jvm >= 0.0.%{year}.%{month}
Requires:  nqp-jvm >= 0.0.%{year}.%{month}
%endif


# Needed for desktop-file-install usage
BuildRequires:  desktop-file-utils


# Replacing existing "rakudo" package
Obsoletes:      rakudo <= 0.0.2010.08_2.7.0-2
Provides:       rakudo = %{version}-%{release}


# filter out the perl5 modules requires for perl6 modules
%filter_from_requires /perl(/d; /perl6/d
%filter_setup


%description
Rakudo Perl 6, or just Rakudo, is a Perl 6 compiler for the Parrot virtual
machine. Rakudo is an implementation of the Perl 6 specification that runs
on the Parrot VM. More information about Perl 6 is available from:
http://perl6.org
Rakudo Star is a collection of things around Rakudo. It installs Perl 6 modules.
The documentation includes a PDF-document that describes the using of Perl 6.


%prep
%setup -q -n %{name}-%{year}.%{month}


%build
%{__perl} Configure.pl --prefix=/usr

# add flags like '-g' to CFLAGS
#%{__sed} -i -e "/^CFLAGS/ s/$/ $RPM_OPT_FLAGS/" Makefile
#%{__sed} -i -e "/^CFLAGS/ s/$/  -O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches  -m64 -mtune=generic/" Makefile

%{__make}  # %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT


# Rakudo installation
%{__sed} -i -e 's&$(DESTDIR)$(DOCDIR)/rakudo&$(DESTDIR)$(DOCDIR)/rakudo-star/rakudo&' rakudo/Makefile

%{__make} rakudo-install DESTDIR=$RPM_BUILD_ROOT

# Generating man-pages
%{__perl} -MExtUtils::Command -e mkpath $RPM_BUILD_ROOT%{_mandir}/man1
pod2man --section=1 --name=perl6 rakudo/docs/running.pod | %{__gzip} -c > $RPM_BUILD_ROOT%{_mandir}/man1/perl6.1.gz
pod2man --section=1 --name=perl6-m rakudo/docs/running.pod | %{__gzip} -c > $RPM_BUILD_ROOT%{_mandir}/man1/perl6-m.1.gz
pod2man --section=1 --name=perl6-j rakudo/docs/running.pod | %{__gzip} -c > $RPM_BUILD_ROOT%{_mandir}/man1/perl6-j.1.gz

export PERL6LIB=$RPM_BUILD_ROOT%{_datadir}/perl6/lib
#%{__make} modules-install DESTDIR=$RPM_BUILD_ROOT

%{__mkdir} -p m_install/usr/bin
%{__ln_s} ../../../perl6 m_install/usr/bin/perl6
%{__make} modules-install DESTDIR=$( pwd )/m_install

# Workaround
%{__mkdir_p} $( pwd )/m_install%{_datadir}/perl6/lib

# Now copy to $RPM_BUILD_ROOT
%{__cp} -r m_install/usr/bin/* $RPM_BUILD_ROOT/usr/bin
%{__cp} -r $( pwd )/m_install/usr/share/perl6/lib/*  $RPM_BUILD_ROOT%{_datadir}/perl6/lib/

# Vielleicht zuerst eingenes nqp bauen
#cd nqp-%{year}.%{month}
#perl Configure.pl
#make
#cd ..

# First install modules files to "m_install" subdirectory und then copy it
# to $RPM_BUILD_ROOT, to avoid having the $RPM_BUILD_ROOT in installed files
#export PERL6LIB=$( pwd )/m_install%{parrot_lang_perl6}/lib:$( pwd )/rakudo/lib

#cp -r rakudo/blib/Perl6 .
#cp rakudo/*.pbc .

#export LD_LIBRARY_PATH=$( pwd )/rakudo/dynext

# move ufo
#%{__mv} m_install/usr/bin m_install%{parrot_lang_perl6}



# Force executable permission on shared objects so they get stripped
%{__chmod} 755 $RPM_BUILD_ROOT%{_datadir}/perl6/runtime/dynext/libperl6*.so
%{__strip} $RPM_BUILD_ROOT%{_datadir}/perl6/runtime/dynext/libperl6*.so


# install desktop files for specs-URL and UsingPerl6-PDF-document
%define DESK_TARGET $RPM_BUILD_ROOT%{_datadir}/applications/
%{__mkdir} -p %{DESK_TARGET}
%{__tar} xzf %{SOURCE1} --directory=%{DESK_TARGET}

desktop-file-install --delete-original --add-category="Documentation"  \
    --dir=%{DESK_TARGET} %{DESK_TARGET}perl6_specs_link.desktop
desktop-file-install --delete-original --add-category="Documentation"  \
    --dir=%{DESK_TARGET} %{DESK_TARGET}rakudo_guide_pdf.desktop

rm -f $RPM_BUILD_ROOT/%{_bindir}/perl6
ln -s perl6-m $RPM_BUILD_ROOT/%{_bindir}/perl6


%check
%{?!_without_tests:
%{__make} rakudo-test

exit 0
# testing the modules
#export PERL6LIB=$( pwd )/m_install%{parrot_lang_perl6}/lib:$( pwd )/rakudo/lib
#export LD_LIBRARY_PATH=$( pwd )/rakudo/dynext
#%{__cp} rakudo/Test.p* m_install%{parrot_lang_perl6}/lib
#
#prove -e ./perl6 modules/Bailador/t
#prove -e ./perl6 -r modules/DBIish/t
#prove -e ./perl6 -r modules/doc/t
#prove -e ./perl6 -r modules/json/t
#prove -e ./perl6 -r modules/jsonrpc/t
prove -e ./perl6-p -r modules/Math-Model/t
prove -e ./perl6-p -r modules/Math-RungeKutta/t
#prove -e ./perl6 -r modules/panda/t
prove -e ./perl6 -r modules/perl6-digest-md5/t
#prove -e ./perl6 -r modules/perl6-File-Tools/t
#prove -e ./perl6 -r modules/perl6-http-easy/???
#prove -e ./perl6 -r modules/perl6-http-status/t
# this test fails with koji
#    prove -e ./perl6 -r modules/perl6-lwp-simple/t
prove -e ./perl6 -r modules/Perl6-MIME-Base64/t
prove -e ./perl6 -r modules/perl6-Term-ANSIColor/t
prove -e ./perl6 -r modules/svg/t
prove -e ./perl6 -r modules/svg-plot/t
#prove -e ./perl6 -r modules/Template-Mojo/t
prove -e ./perl6 -r modules/test-mock/t
prove -e ./perl6 -r modules/uri/t
prove -e ./perl6 -r modules/xml-writer/t
#prove -e ./perl6 -r modules/zavolaj/t
}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#
%doc LICENSE README docs/CREDITS docs/cheatsheet.txt docs/2015-spw-perl6-course.pdf
%{_bindir}/perl6
%{_bindir}/perl6-m
%{_bindir}/perl6-debug-m
%{_bindir}/perl6-gdb-m
%{_bindir}/perl6-valgrind-m

%{_datadir}/nqp/lib/Perl6
%{_datadir}/perl6/lib/*
%{_datadir}/perl6/runtime/*
%{_mandir}/man1/perl6.1.gz
%{_mandir}/man1/perl6-m.1.gz
%{_mandir}/man1/perl6-j.1.gz


# modules part
# %%{_bindir}/ufo is moved to %%{parrot_lang_perl6}/bin/ufo
# the other modules files are in %%{parrot_lang_perl6}/lib placed with
# %%{parrot_lang_perl6} above

# desktop files
%{_datadir}/applications/perl6_specs_link.desktop
%{_datadir}/applications/rakudo_guide_pdf.desktop

# Module files
%{_bindir}/p6doc*
%{_bindir}/panda*
%{_bindir}/ufo*

# JVM files
%if %{build_jvm_exec}
%{_bindir}/perl6-j
%{_bindir}/perl6-debug-j
%{_bindir}/perl6-eval-server
%{_bindir}/perl6-jdb-server
%{_datadir}/perl6/lib
%{_datadir}/perl6/lib/Perl6
%{_datadir}/perl6/runtime/dynext
%{_datadir}/perl6/runtime/*.moarvm
%endif


%changelog
