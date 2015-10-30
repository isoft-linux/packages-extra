Name:           ecj 
Version:        4.3.2
Release:        2
Summary:        Eclipse Compiler for Java
License:        GPL
Source0:        %{name}-%{version}.jar
Source1:        ecj

Requires:       jamvm 

%description
Eclipse Compiler for Java
%prep


%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/ecj
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/ecj/
install -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ecj
pushd $RPM_BUILD_ROOT%{_datadir}/ecj/
ln -s %{name}-%{version}.jar ecj.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_datadir}/ecj
%{_datadir}/ecj/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.3.2-2
- Rebuild

