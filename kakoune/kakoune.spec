Name: kakoune 
Version: 0.1 
Release: 2.git
Summary: Another Vim-Inspired Code Editor

License: Public Domain
URL: http://kakoune.org/ 
Source0: %{name}.tar.gz

BuildRequires:  boost-devel >= 1.50
BuildRequires:  ncurses-devel >= 5.3

%description
Kakoune is a command-line code editor that's inspired by Vim
and its advertised features are support for multiple selections, 
many customization possibilities, a client/server architecture so 
many clients can collaboratively edit the contents of a file, 
and advanced text manipulation primitives. 

%prep
%setup -q -n %{name}

%build
cd src
make %{?_smp_mflags}

%install
cd src
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%check
cd src
make test

%files
%{_bindir}/*
%{_datadir}/doc/kak/*
%{_datadir}/kak/*

%changelog
* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 0.1-2.git
- Initial build


