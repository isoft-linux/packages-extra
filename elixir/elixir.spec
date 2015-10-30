Name:           elixir
Version:        1.1.1
Release:        2%{?dist}
Summary:        A modern approach to programming for the Erlang VM 

License:        ASL 2.0 and ERPL
URL:            http://elixir-lang.org/

Source0:        https://github.com/elixir-lang/elixir/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  erlang
BuildRequires:  git
Requires:       erlang

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

%prep
%setup -q

%build
LANG="en_US.UTF-8";  make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}
cp -ra bin lib %{buildroot}/%{_datadir}/%{name}/%{version}

mkdir -p %{buildroot}/%{_bindir}
ln -s %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}/%{_bindir}/

%check
LANG="en_US.utf8" make test

%files
%doc LICENSE LEGAL
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.1.1-2
- Rebuild

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- initial build.
