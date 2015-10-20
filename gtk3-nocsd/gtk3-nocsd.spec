Name: gtk3-nocsd 
Version: 2.0
Release: 1.git
Summary: A hack to disable gtk+ 3 client side decoration

License: LGPL
URL: https://github.com/PCMan/gtk3-nocsd
Source0: %{name}.tar.gz

BuildRequires: gtk3-devel
Requires: gtk3

%description
A hack to disable gtk+ 3 client side decoration

%prep
%setup -q -n %{name} 

%build
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} prefix=/usr


%files
%{_bindir}/gtk3-nocsd
%{_mandir}/man1/*
%{_libdir}/libgtk3-nocsd.so.0

%changelog
* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- initial build.
