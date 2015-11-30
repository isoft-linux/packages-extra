Name:           cabextract
Version:        1.5
Release:        2%{?dist}
Summary:        Utility for extracting cabinet (.cab) archives

License:        GPLv2+
URL:            http://www.cabextract.org.uk/
Source:         http://www.cabextract.org.uk/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libmspack-devel


%description
cabextract is a program which can extract files from cabinet (.cab)
archives.


%prep
%setup -q


%build
%configure --with-external-libmspack

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/cabextract
%{_mandir}/man1/cabextract.1*


%changelog
* Mon Nov 30 2015 Cjacker <cjacker@foxmail.com> - 1.5-2
- Initial build

