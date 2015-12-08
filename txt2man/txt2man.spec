Name:           txt2man
Version:        1.5.6
Release:        2%{?dist}
Summary:        Convert flat ASCII text to man page format

License:        GPLv2+
URL:            http://mvertes.free.fr/txt2man/
Source0:        http://mvertes.free.fr/download/%{name}-%{version}.tar.gz
Patch1:         txt2man-1.5.6-fixbashisms.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       gawk

%description
tx2man is a shell script using gnu awk, that should run on any
Unix-like system. The syntax of the ASCII text is very straightforward
and looks very much like the output of the man(1) program. 

%prep
%setup -q
%patch1

%build
#no build needed

%install
rm -rf $RPM_BUILD_ROOT
#manual install
install -p -m 0755 -D bookman $RPM_BUILD_ROOT%{_bindir}/bookman
install -p -m 0755 -D src2man $RPM_BUILD_ROOT%{_bindir}/src2man
install -p -m 0755 -D txt2man $RPM_BUILD_ROOT%{_bindir}/txt2man

install -p -m 0644 -D bookman.1 $RPM_BUILD_ROOT%{_mandir}/man1/bookman.1
install -p -m 0644 -D src2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/src2man.1
install -p -m 0644 -D txt2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/txt2man.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Changelog README
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.5.6-2
- Initial build

