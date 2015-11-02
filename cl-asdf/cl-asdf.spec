Name:    cl-asdf
Version: 20101028
Release: 10%{?dist}
Source:  %{name}-%{version}.tar.bz2
Summary: Another System Definition Facility
URL:     http://www.cliki.net/asdf
License: MIT
BuildArch: noarch

Patch0:  cl-asdf-20101028-texinfo5.patch

%description
Another System Definition Facility (asdf) is a package format for
Common Lisp libraries.

%prep
%setup -q -n asdf
%patch0 -p1

%install
mkdir -m 755 -p %{buildroot}%{_datadir}/common-lisp/source/cl-asdf
install -m 644 asdf.lisp %{buildroot}%{_datadir}/common-lisp/source/cl-asdf
install -m 644 wild-modules.lisp %{buildroot}%{_datadir}/common-lisp/source/cl-asdf

%build

%files
%doc README
%dir %{_datadir}/common-lisp
%dir %{_datadir}/common-lisp/source
%{_datadir}/common-lisp/source/cl-asdf

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 20101028-10
- Initial build

