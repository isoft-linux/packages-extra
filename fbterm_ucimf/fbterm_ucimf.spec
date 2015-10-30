Name:		fbterm_ucimf
Version:	0.2.9
Release:	2
Summary:	fbterm ucimf input plugin

License:	GPLv2+
URL:		https://code.google.com/p/ucimf
Source0:	https://ucimf.googlecode.com/files/fbterm_ucimf-0.2.9.tar.gz

BuildRequires:	libucimf-devel
#require it.
Requires:	ucimf-openvanilla

%description
%{summary}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/fbterm_ucimf
%{_mandir}/man1/fbterm_ucimf.1.gz

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.9-2
- Rebuild


