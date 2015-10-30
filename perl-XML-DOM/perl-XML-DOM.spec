Name:           perl-XML-DOM
Version:        1.45
Release:        2%{?dist}
Summary:        DOM extension to XML::Parser

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-DOM/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-DOM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(XML::Parser) >= 2.30
BuildRequires:  perl(XML::RegExp)
# Tests:
BuildRequires:  perl(Test)
BuildRequires:  perl(utf8)
BuildRequires:  perl(XML::Parser::PerlSAX) >= 0.07
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(XML::Parser) >= 2.30
Obsoletes:      perl-libxml-enno <= 1.02

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::XQL::Node\\)

%description
This is a Perl extension to XML::Parser. It adds a new 'Style' to
XML::Parser, called 'DOM', that allows XML::Parser to build an Object
Oriented data structure with a DOM Level 1 compliant interface. For a
description of the DOM (Document Object Model), see
<http://www.w3.org/DOM/>.


%prep
%setup -q -n XML-DOM-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
#make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc BUGS Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::*.3*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.45-2
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build. 

