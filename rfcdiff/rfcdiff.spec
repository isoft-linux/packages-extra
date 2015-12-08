Name:           rfcdiff
Version:        1.41
Release:        2%{?dist}
Summary:        Compares two internet draft files and outputs the difference

License:        GPLv2+
URL:            http://tools.ietf.org/tools/rfcdiff/
Source0:        http://tools.ietf.org/tools/rfcdiff/%{name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  txt2man

%description
The purpose of this program is to compare two versions of an
internet-draft, and as output produce a diff in one of several
formats:
- side-by-side html diff
- paged wdiff output in a text terminal
- a text file with changebars in the left margin
- a simple unified diff output

In all cases, internet-draft headers and footers are stripped before
generating the diff, to produce a cleaner diff.


%prep
%setup -q
sed -i 's|include ../Makefile.common|include Makefile.common|g' Makefile

%build
make manpage


%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man1

install -pm 0755 %{name} %{buildroot}%{_bindir}/
install -pm 0644 %{name}.1.gz %{buildroot}%{_mandir}/man1/


%files
%doc changelog copyright todo
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz


%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.41-2
- Initial build

