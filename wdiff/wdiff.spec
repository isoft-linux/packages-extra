Name:           wdiff
Version:        1.2.2
Release:        2%{?dist}
Summary:        A front-end to GNU diff

License:        GPLv3+
URL:            http://www.gnu.org/software/%{name}/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libtool  
BuildRequires:  texinfo  

%description
`wdiff' is a front-end to GNU `diff'.  It compares two files, finding
which words have been deleted or added to the first in order to create
the second.  It has many output formats and interacts well with
terminals and pagers (notably with `less').  `wdiff' is particularly
useful when two texts differ only by a few words and paragraphs have
been refilled.

%prep
%setup -q -n %{name}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 ChangeLog > ChangeLog.new && \
touch -r ChangeLog ChangeLog.new && \
mv ChangeLog.new ChangeLog

%build
%configure --enable-experimental="mdiff wdiff2 unify" 
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf $RPM_BUILD_ROOT%{_infodir}
find $RPM_BUILD_ROOT -type f -name '*gnulib.mo' -exec rm -f {} ';'

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc NEWS  README TODO  ChangeLog  AUTHORS
%{_bindir}/*
%{_mandir}/man1/*.1.gz


%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.2.2-2
- Initial build

