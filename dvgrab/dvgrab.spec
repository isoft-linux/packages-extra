Summary:        Utility to capture video from a DV camera
Name:           dvgrab
Version:        3.5
Release:        15%{?dist}
License:        GPLv2+
URL:            http://www.kinodv.org/
Source:         http://downloads.sourceforge.net/project/kino/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libraw1394-devel libavc1394-devel libdv-devel
BuildRequires:  libiec61883-devel libjpeg-devel
ExcludeArch:    s390 s390x

%description
The dvgrab utility will capture digital video from a DV source on the firewire
(IEEE-1394) bus.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README COPYING ChangeLog NEWS
%{_bindir}/dvgrab
%{_mandir}/man1/dvgrab.1*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.5-15
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 3.5-14
- Initial build.
