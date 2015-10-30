Name:		axel		
Version:	2.4
Release:	13%{?dist}
Summary:	Accelerated download client

License:	GPLv2+
URL:		http://axel.alioth.debian.org/
Source0:	http://alioth.debian.org/frs/download.php/3015/%{name}-%{version}.tar.gz
BuildRequires:	gettext



%description
Axel tries to accelerate HTTP/FTP downloading process by using 
multiple connections for one file. It can use multiple mirrors for a 
download. Axel has no dependencies and is lightweight, so it might 
be useful as a wget clone on byte-critical systems.

%prep
%setup -q

%build
export CFLAGS=" %{optflags}"
export CXXFLAGS=" %{optflags}"
./configure --prefix=%{_prefix} --strip=0
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install \
	DESTDIR=%{buildroot}

install -m 755 -p %{name} %{buildroot}%{_bindir}

%find_lang	%{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc CHANGES CREDITS API README COPYING
%config(noreplace) %{_sysconfdir}/axelrc
%{_mandir}/man1/axel.1*
%{_mandir}/zh_CN/man1/axel.1*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.4-13
- Rebuild

