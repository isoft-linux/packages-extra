Name:		fbterm_ucimf
Version:	0.2.9
Release:	1
Summary:	fbterm ucimf input plugin

Group:		Core/Runtime/Library
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

rpmclean
%files
%{_bindir}/fbterm_ucimf
%{_mandir}/man1/fbterm_ucimf.1.gz

%changelog

