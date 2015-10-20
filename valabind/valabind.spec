Name: valabind 
Version: 0.9.2
Release: 1
Summary: A tool to parse vala or vapi files to swig interface files

License: GPLv3 
URL: https://github.com/radare/valabind
Source0: http://rada.re/get/valabind-%{version}.tar.gz 

BuildRequires: vala vala-devel

%description
%{Summary}

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/*
%{_mandir}/man*/*

%changelog
* Sat Oct 10 2015 Cjacker <cjacker@foxmail.com>
- initial package
