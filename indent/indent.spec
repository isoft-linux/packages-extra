Summary: A GNU program for formatting C code
Name: indent
Version: 2.2.10
Release: 2
License: GPLv3+
URL: http://indent.isidore-it.eu/beautify.html
Source: http://indent.isidore-it.eu/%{name}-%{version}.tar.gz
Patch3: indent-2.2.9-explicits.patch
Patch4: indent-2.2.9-cdw.patch
Patch5: indent-2.2.9-lcall.patch
Patch7: indent-2.2.9-man.patch
BuildRequires: gettext

%description
Indent is a GNU program for beautifying C code, so that it is easier to
read.  Indent can also convert from one C writing style to a different
one.  Indent understands correct C syntax and tries to handle incorrect
C syntax.

Install the indent package if you are developing applications in C and
you want a program to format your code.

%prep
%setup -q
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1

%build
export CC=clang
export CXX=clang++

%configure
echo "all:" >doc/Makefile
echo "install:" >>doc/Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir $RPM_BUILD_ROOT/%{_bindir}/texinfo2man \
	$RPM_BUILD_ROOT/usr/doc/indent/indent.html

%find_lang %name
%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/indent
%{_mandir}/man1/indent.*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.2.10-2
- Rebuild

