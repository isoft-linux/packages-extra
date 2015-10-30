Name:           perl-DBD-MySQL
Version:        4.033
Release:        1%{?dist}
Summary:        A MySQL interface for Perl
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-mysql/
Source0:        http://www.cpan.org/authors/id/C/CA/CAPTTOFU/DBD-mysql-%{version}.tar.gz
BuildRequires:  mariadb, mariadb-devel, zlib-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI) >= 1.08
BuildRequires:  perl(DBI::DBD)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl-DBD-mysql = %{version}-%{release}

%{?perl_default_filter}

%description 
DBD::mysql is the Perl5 Database Interface driver for the MySQL database. In
other words: DBD::mysql is an interface between the Perl programming language
and the MySQL programming API that comes with the MySQL relational database
management system.

%prep
%setup -q -n DBD-mysql-%{version}
# Correct file permissions
find . -type f | xargs chmod -x

for file in lib/DBD/mysql.pm ChangeLog; do
  iconv -f iso-8859-1 -t utf-8 <$file >${file}_
  touch -r ${file}{,_}
  mv -f ${file}{_,}
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" --ssl
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
# Full test coverage requires a live MySQL database
#make test

%files
%license LICENSE
%doc ChangeLog eg README.pod TODO
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{_mandir}/man3/*.3*

%changelog
