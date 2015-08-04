Name:          perl-Font-TTF
Version:       1.05
Release:       3%{?dist}
Summary:       Perl library for modifying TTF font files
Group:         Development/Libraries
License:       Artistic 2.0
URL:           http://search.cpan.org/dist/Font-TTF/
Source0:       http://cpan.org/authors/id/M/MH/MHOSKEN/Font-TTF-%{version}.tar.gz
BuildArch:     noarch
# Build
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires: perl(Getopt::Std)
BuildRequires: perl(strict)
# Runtime
BuildRequires: perl(bytes)
BuildRequires: perl(Compress::Zlib)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::String)
BuildRequires: perl(Symbol)
BuildRequires: perl(utf8)
BuildRequires: perl(vars)
# Unused BuildRequires: perl(XML::Parser::Expat)
# Tests only
BuildRequires: perl(File::Compare)
BuildRequires: perl(Test::Simple)

BuildRequires: perl(vars)
Requires: perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
Perl module for TrueType font hacking. Supports reading, processing and writing
of the following tables: GDEF, GPOS, GSUB, LTSH, OS/2, PCLT, bsln, cmap, cvt,
fdsc, feat, fpgm, glyf, hdmx, head, hhea, hmtx, kern, loca, maxp, mort, name,
post, prep, prop, vhea, vmtx and the reading and writing of all other table
types.

In short, you can do almost anything with a standard TrueType font with this
module.

%prep
%setup -q -n Font-TTF-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} +
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc README.TXT CONTRIBUTORS Changes TODO
%dir %{perl_vendorlib}/Font
%dir %{perl_vendorlib}/Font/TTF
%{perl_vendorlib}/ttfmod.pl
%{perl_vendorlib}/Font/TTF.pm
%{perl_vendorlib}/Font/TTF/*
%{_mandir}/man3/*.3*
# We really don't want to use this perl package in a Win32 env
# or poke in the windows registry to resolve fonts
# (upstream makefile needs to get smarter)
%exclude %{perl_vendorlib}/Font/TTF/Win32.pm

%changelog
