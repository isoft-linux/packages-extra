Name:           sourcenavigator 
Version:        4.5 
Release:        2 
Summary:        source navigator NG is a source code analysis tool.
License:        GPLv2+
URL:            http://sourcenav.sourceforge.net/
Source0:        %{name}-NG%{version}.tar.bz2

%description
source navigator NG is a source code analysis tool.

%prep
%setup -q -n %{name}-NG%{version}

%build
./configure --prefix=/opt/sourcenavigator
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
/opt/sourcenavigator

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 4.5-2
- Rebuild

