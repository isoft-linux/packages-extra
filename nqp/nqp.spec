#
# noarch:            nqp with moar
#


%global year 2015
%global month 11


Name:		nqp
Version:	0.0.%{year}.%{month}
Release:	2%{?dist}
Summary:	Not Quite Perl (6)

BuildArch:	noarch

License:	Artistic 2.0 and ISC and WTFPL
URL:		https://github.com/perl6/nqp
Source0:	http://rakudo.org/downloads/nqp/nqp-%{year}.%{month}.tar.gz

BuildRequires:	perl(Test::Harness)
BuildRequires:	perl(ExtUtils::Command)

BuildRequires:	moarvm
BuildRequires:	moarvm-devel

Requires:	moarvm


%description
This is "Not Quite Perl" -- a lightweight Perl 6-like environment for virtual
machines. The key feature of NQP is that it's designed to be a very small
environment (as compared with, say, perl6 or Rakudo) and is focused on being
a high-level way to create compilers and libraries for virtual machines (such
as JVM and MoarVM). Unlike a full-fledged implementation of Perl 6, NQP
strives to have as small a runtime footprint as it can, while still providing
a Perl 6 object model and regular expression engine for the virtual machine.


#--

%package doc
Summary:	Documentation for Not Quite Perl (6)

BuildArch:	noarch


%description doc
Documentation and also examples about NQP.

#--


%prep
%setup -q -n %{name}-%{year}.%{month}


%build
%{__perl} Configure.pl --backends=moar --prefix=%{_usr}
CFLAGS="$RPM_OPT_FLAGS -fPIC" %{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT


%check
# fails at prove -r --exec "./nqp-m" ...
#rm -f t/hll/06-sprintf.t
%{?!_without_tests: make test}


%files
%doc CREDITS LICENSE README.pod
%{_bindir}/nqp
%{_bindir}/nqp-m
%dir %{_datadir}/nqp
%dir %{_datadir}/nqp/lib
%{_datadir}/nqp/lib/*.moarvm
%{_datadir}/nqp/lib/profiler/template.html


%files doc
%doc docs examples


%changelog
* Sat Dec 26 2015 Cjacker <cjacker@foxmail.com> - 0.0.2015.11-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.0.2015.09.1-2
- Rebuild

