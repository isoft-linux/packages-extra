Name:           perl-Taint-Runtime
Version:        0.03
Release:        25%{?dist}
Summary:        Runtime enable taint checking
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Taint-Runtime
Source0:        http://search.cpan.org/CPAN/authors/id/R/RH/RHANDOM/Taint-Runtime-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)

%{?perl_default_filter}

%description
This module enables run-time taint checking, for cases where the -T
switch on the command line is not appropriate or viable. There are
a somewhat limited number of legitimate use cases where you should 
use this module instead of the -T switch. Unless you have a specific and
good reason for not using the -T option, you should use the -T option.

%prep
%setup -q -n Taint-Runtime-%{version}
chmod +x is_taint_bench.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Taint/
%{perl_vendorarch}/Taint/
%{_mandir}/man3/*.3*

%changelog
