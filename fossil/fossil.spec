Name:		fossil
Version:	20140612172556
Release:	1
Summary:	Simple, high-reliability, distributed software configuration management

Group:		CoreDev/Development/Utility
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

rpmclean
%files
%{_bindir}/fossil

%changelog

