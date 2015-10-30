Name:           bakefile
Version:        0.2.9
Release:        9%{?dist}
Summary:        A cross-platform, cross-compiler native makefiles generator
License:        MIT
URL:            http://www.bakefile.org/
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         bakefile-028-fix-import.patch
Patch1:         bakefile-format-security.patch

BuildRequires:  python-libxml2 python-devel
Requires:       python >= 2.3.0 automake python-empy

%description
Bakefile is cross-platform, cross-compiler native makefiles generator. It takes
compiler-independent description of build tasks as input and generates native
makefile (autoconf's Makefile.in, Visual C++ project, bcc makefile etc.)

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README THANKS
%{_bindir}/bakefil*
%{_datadir}/bakefile
%{_mandir}/man1/bakefil*
%{_libdir}/bakefile*
%exclude %{_libdir}/%{name}/empy
%exclude %{_libdir}/%{name}/py25modules
%exclude %{_libdir}/%{name}/_bkl_c.la
%{_datadir}/aclocal/*.m4

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.9-9
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 0.2.9-8
- Initial build.

