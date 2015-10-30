Name:		fossil
Version:	20140612172556
Release:	2
Summary:	Simple, high-reliability, distributed software configuration management

License:    BSD2	
URL:		http://www.fossil-scm.org
Source0:	%{name}-src-%{version}.tar.gz

%description
%{summary}

%prep
%setup -q -n %{name}-src-%{version}

%build
./configure --prefix=/usr --sysconfdir=/etc

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/fossil

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 20140612172556-2
- Rebuild


