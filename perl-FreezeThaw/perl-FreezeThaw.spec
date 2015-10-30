Name:           perl-FreezeThaw
Version:        0.5001
Release:        16%{?dist}
Summary:        Convert Perl structures to strings and back
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/FreezeThaw/
Source0:        http://www.cpan.org/authors/id/I/IL/ILYAZ/modules/FreezeThaw-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Math::BigInt)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Converts data to/from stringified form, appropriate for
saving-to/reading-from permanent storage.

%prep
%setup -q -n FreezeThaw-%{version}
# Fix permissions
find -type d -exec chmod 0755 {} \;
find -type f -exec chmod 0644 {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3pm*

%changelog
