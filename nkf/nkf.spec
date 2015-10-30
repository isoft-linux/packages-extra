Name:		nkf
Epoch:		1
Version:	2.1.3
Release:	8%{?dist}
License:	BSD
URL:		http://nkf.sourceforge.jp/
Source0:	http://osdn.dl.sourceforge.jp/nkf/59912/%{name}-%{version}.tar.gz
## snippet from the source code
Source3:	nkf.copyright
Source4:	nkf.1j
BuildRequires:	perl(ExtUtils::MakeMaker)

Summary:	A Kanji code conversion filter

%description
Nkf is a Kanji code converter for terminals, hosts, and networks. Nkf
converts input Kanji code to 7-bit JIS, MS-kanji (shifted-JIS) or
EUC.

%package -n perl-NKF
Summary:	Perl extension for Network Kanji Filter
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-NKF
This is a Perl Extension version of nkf (Network Kanji Filter).
It converts the last argument and return converted result.
Conversion details are specified by flags before the last argument.

%prep
%setup -q
cp -p %{SOURCE4} .

%build
make CFLAGS="$RPM_OPT_FLAGS" nkf
cp -p %{SOURCE3} .
pushd NKF.mod
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=%{_prefix} INSTALLDIRS=vendor
make %{?_smp_mflags}
popd

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man1,ja/man1}

./nkf -e nkf.1j > nkf.1jeuc
iconv -f euc-jp -t utf-8 nkf.1jeuc > nkf.1utf8
touch -r nkf.1j nkf.1utf8
install -m 755 -p nkf $RPM_BUILD_ROOT%{_bindir}
install -m 644 -p nkf.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p nkf.1utf8 $RPM_BUILD_ROOT%{_mandir}/ja/man1/nkf.1
pushd NKF.mod
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"
rm -f	$RPM_BUILD_ROOT%{perl_vendorarch}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod		\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.bs	\
	$RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/.packlist
popd
chmod 0755 $RPM_BUILD_ROOT%{perl_vendorarch}/auto/NKF/NKF.so


%check
make test

%files
%doc nkf.doc nkf.copyright
%{_bindir}/nkf
%{_mandir}/man1/nkf.1*
%{_mandir}/ja/man1/nkf.1*

%files -n perl-NKF
%doc nkf.doc nkf.copyright
%{perl_vendorarch}/NKF.pm
%{perl_vendorarch}/auto/*
%{_mandir}/man3/NKF.3pm.gz

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1:2.1.3-8
- Rebuild

