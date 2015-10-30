Name:           perl-MLDBM
Version:        2.05
Release:        7%{?dist}
Summary:        Store multi-level hash structure in single level tied hash
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/MLDBM/
Source0:        http://www.cpan.org/authors/id/C/CH/CHORNY/MLDBM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper) >= 2.08
BuildRequires:  perl(FreezeThaw)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module can serve as a transparent interface to any TIEHASH package
that is required to store arbitrary perl data, including nested references.
Thus, this module can be used for storing references and other arbitrary
data within DBM databases.

%prep
%setup -q -n MLDBM-%{version}

# Fix line endings for documentation
sed -i -e 's/\r$//' README Changes

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes README
%{perl_vendorlib}/MLDBM/
%{perl_vendorlib}/MLDBM.pm
%{_mandir}/man3/MLDBM.3pm*

%changelog
