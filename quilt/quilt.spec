%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		quilt
Summary:	Scripts for working with series of patches
License:	GPLv2
Group:		Development/Tools
Version:	0.64
Release:	4
Source:		http://savannah.nongnu.org/download/quilt/quilt-%{version}.tar.gz
URL:		http://savannah.nongnu.org/projects/quilt
BuildRequires: gettext gawk util-linux-ng
BuildArch: noarch
Obsoletes: quilt <= 0.51-1
Requires: coreutils
Requires: diffutils
Requires: gzip
Requires: bzip2
Requires: sed
Requires: gawk
Requires: diffstat
Requires: %{_sbindir}/sendmail
Requires: util-linux-ng
Requires: tar
Requires: rpm-build
Requires: procmail

%description
These scripts allow one to manage a series of patches by keeping track of the
changes each patch makes. Patches can be applied, un-applied, refreshed, etc.

The scripts are heavily based on Andrew Morton's patch scripts found at
http://www.zip.com.au/~akpm/linux/patches/

%prep
%setup

%build
%configure --with-sendmail=%{_sbindir}/sendmail --with-diffstat=%{_bindir}/diffstat --docdir=%{_pkgdocdir}
make %{?_smp_mflags}

%install
make install BUILD_ROOT=$RPM_BUILD_ROOT
%{find_lang} %{name}
mv $RPM_BUILD_ROOT/%{_pkgdocdir}/* .
rm -rf $RPM_BUILD_ROOT/%{_pkgdocdir}

%files -f %{name}.lang
%defattr(-, root, root)
%doc README README.MAIL quilt.pdf
%doc AUTHORS COPYING TODO
%{_bindir}/guards
%{_bindir}/quilt
%{_datadir}/quilt/
%{_datadir}/emacs/site-lisp/quilt.el
%{_sysconfdir}/bash_completion.d
%config %{_sysconfdir}/quilt.quiltrc
%{_mandir}/man1/*

%changelog
* Thu Nov 26 2015 xiaotian.wu@i-soft.com.cn - 0.64-4
- rebuilt

* Thu Nov 12 2015 xiaotian.wu@i-soft.com.cn - 0.64-3
- init for isoft
