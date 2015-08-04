Name:		perl-Text-CSV
Version:	1.21
Release:	7
Summary:	Comma-separated values manipulator

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Text-CSV/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MA/MAKAMAKA/Text-CSV-%{version}.tar.gz
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(IO::Handle)

BuildArch:	noarch

BuildRequires:	perl(ExtUtils::MakeMaker)

# For test suite
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Test::Harness)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(IO::Handle)

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

The module accepts either strings or files as input and can utilize any
user-specified characters as delimiters, separators, and escapes so it is
perhaps better called ASV (anything separated values) rather than just CSV.

%prep
%setup -q -n Text-CSV-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%check
%{__make} test TEST_VERBOSE=1

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

