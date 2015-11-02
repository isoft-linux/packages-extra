Summary:      Common Lisp source and compiler manager
Name:         common-lisp-controller
Version:      7.4
Release:      10%{?dist}
URL:          https://alioth.debian.org/projects/clc
Source0:      http://ftp.de.debian.org/debian/pool/main/c/common-lisp-controller/common-lisp-controller_%{version}.tar.gz
Patch0:       common-lisp-controller-isoft.patch
License:      LLGPL
BuildArch:    noarch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:     cl-asdf

%description
This package helps installing Common Lisp sources and compilers.
It creates a user-specific cache of compiled objects. When a library
or an implementation is upgraded, all compiled objects in the cache
are flushed. It also provides tools to recompile all libraries.

%prep 
%setup -q
%patch0 -p0 

%build
# Do nothing.

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/common-lisp
install -dm 755 $RPM_BUILD_ROOT%{_prefix}/sbin
install -dm 755 $RPM_BUILD_ROOT%{_bindir}
install -dm 755 $RPM_BUILD_ROOT%{_sbindir}
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/man/man1
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/man/man3
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/man/man8
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/common-lisp
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/common-lisp/systems
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/common-lisp/source
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/common-lisp-controller
install -dm 755 $RPM_BUILD_ROOT%{_localstatedir}
install -dm 755 $RPM_BUILD_ROOT%{_localstatedir}/cache
install -dm 1777 $RPM_BUILD_ROOT%{_localstatedir}/cache/common-lisp-controller
# Not %{_libdir} because we really want /usr/lib even on 64-bit systems.
install -dm 755 $RPM_BUILD_ROOT/usr/lib/common-lisp
install -dm 755 $RPM_BUILD_ROOT/usr/lib/common-lisp/bin

for f in register-common-lisp-source unregister-common-lisp-source \
        register-common-lisp-implementation \
        unregister-common-lisp-implementation clc-update-customized-images; do
        install -m 755 $f $RPM_BUILD_ROOT%{_sbindir};
done;

for f in clc-register-user-package clc-unregister-user-package \
         clc-clbuild clc-lisp clc-slime; do
        install -m 755 $f $RPM_BUILD_ROOT%{_bindir};
done;

for f in common-lisp-controller.lisp post-sysdef-install.lisp; do
        install -m 644 $f $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/common-lisp-controller;
done;

install -m 644 lisp-config.lisp -p -D $RPM_BUILD_ROOT%{_sysconfdir}/lisp-config.lisp

gzip man/*
install -m 644 man/register-common-lisp-implementation.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 man/clc-register-user-package.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 man/clc-clbuild.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 man/clc-lisp.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 man/clc-slime.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 man/common-lisp-controller.3.gz $RPM_BUILD_ROOT/%{_mandir}/man3

cd man
ln -s register-common-lisp-implementation.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/unregister-common-lisp-implementation.8.gz
ln -s register-common-lisp-implementation.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/register-common-lisp-source.8.gz
ln -s register-common-lisp-implementation.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/unregister-common-lisp-source.8.gz
ln -s register-common-lisp-implementation.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/clc-update-customized-images.8.gz
ln -s clc-register-user-package.1.gz  $RPM_BUILD_ROOT/%{_mandir}/man1/clc-unregister-user-package.1.gz
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

# Think about it -- Rex
#triggerin -- sbcl
#/usr/sbin/register-common-lisp-implementation sbcl > /dev/null ||:

%files
%defattr(-,root,root)
%doc DESIGN.txt debian/copyright
%dir %{_sysconfdir}/common-lisp
%dir /usr/lib/common-lisp
%dir /usr/lib/common-lisp/bin
%dir %{_localstatedir}/cache/common-lisp-controller
%config(noreplace) %{_sysconfdir}/lisp-config.lisp
%{_datadir}/common-lisp
%{_bindir}/clc-*
%{_sbindir}/clc-*
%{_sbindir}/register-*
%{_sbindir}/unregister-*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 7.4-10
- Initial build

