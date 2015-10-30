Name:           perl-GD
Version:        2.56
Release:        5%{?dist}
Summary:        Perl interface to the GD graphics library
License:        GPL+ or Artistic 2.0
URL:            http://search.cpan.org/dist/GD/
Source0:        http://www.cpan.org/authors/id/L/LD/LDS/GD-%{version}.tar.gz
Patch0:         GD-2.56-utf8.patch
# Module Build
BuildRequires:  gd-devel >= 2.0.28
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Module::Build)
# Module Runtime
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(constant)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       gd >= 2.0.28

%{?perl_default_filter}

%description
This is a autoloadable interface module for GD, a popular library
for creating and manipulating PNG files. With this library you can
create PNG images on the fly or modify existing files.

%prep
%setup -q -n GD-%{version}

# Re-code documentation as UTF8
%patch0

# Fix shellbangs in sample scripts
perl -pi -e 's|/usr/local/bin/perl\b|%{__perl}|' \
      demos/{*.{pl,cgi},truetype_test}

%build
perl Build.PL
./Build

%install
./Build install --destdir=%{buildroot} --installdirs=vendor --create_packlist=0
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

# These files should not have been installed
rm %{buildroot}%{_bindir}/bdf2gdfont.PLS \
   %{buildroot}%{_bindir}/README \
   %{buildroot}%{_mandir}/man1/bdf2gdfont.PLS.1*

# This binary is in gd-progs
rm %{buildroot}%{_bindir}/bdftogd

%check
./Build test ||

%files
%license LICENSE
%doc ChangeLog README README.QUICKDRAW demos/
%{_bindir}/bdf2gdfont.pl
# %%{_bindir}/bdftogd
%{_bindir}/cvtbdf.pl
%{perl_vendorarch}/auto/GD/
%{perl_vendorarch}/GD.pm
%{perl_vendorarch}/GD/
%{_mandir}/man1/bdf2gdfont.pl.1*
%{_mandir}/man3/GD.3*
%{_mandir}/man3/GD::Image.3*
%{_mandir}/man3/GD::Polygon.3*
%{_mandir}/man3/GD::Polyline.3*
%{_mandir}/man3/GD::Simple.3*

%changelog
