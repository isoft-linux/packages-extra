Summary: Produces a document with syntax highlighting
Name: source-highlight
Version: 3.1.8
Release: 2%{?dist}
License: GPLv3+
Source0: ftp://ftp.gnu.org/gnu/src-highlite/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/src-highlite/%{name}-%{version}.tar.gz.sig
URL: http://www.gnu.org/software/src-highlite/
BuildRequires: bison, flex, boost-devel
BuildRequires: help2man, ctags, chrpath, pkgconfig(bash-completion)
Requires: ctags

%description
This program, given a source file, produces a document with syntax
highlighting. At the moment this package can handle :
Java, Javascript, C/C++, Prolog, Perl, Php3, Python, Flex, ChangeLog, Ruby, 
Lua, Caml, Sml and Log as source languages, and HTML, XHTML and ANSI color 
escape sequences as output format.


%package devel
Summary: Development files for source-highlight
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for source-highlight

%prep
%setup -q

%build
%configure --disable-static \
           --with-boost-regex=boost_regex
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/doc/ docs
%{__sed} -i 's/\r//' docs/source-highlight/*.css

rm -rf $RPM_BUILD_ROOT%{_infodir}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/source-highlight
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/source-highlight-settings

echo -e "\ncxx = cpp.lang" >> $RPM_BUILD_ROOT%{_datadir}/source-highlight/lang.map

bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p $RPM_BUILD_ROOT$bashcompdir
mv $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/source-highlight \
    $RPM_BUILD_ROOT$bashcompdir/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc docs/source-highlight/*
%{_bindir}/cpp2html
%{_bindir}/java2html
%{_bindir}/source-highlight
%{_bindir}/source-highlight-esc.sh
%{_bindir}/check-regexp
%{_bindir}/source-highlight-settings
%{_bindir}/src-hilite-lesspipe.sh
%{_datadir}/bash-completion/
%{_libdir}/libsource-highlight.so.*
%dir %{_datadir}/source-highlight
%{_datadir}/source-highlight/*
%{_mandir}/man1/*

%files devel
%defattr (-,root,root)
%dir %{_includedir}/srchilite
%{_libdir}/libsource-highlight.so
%{_libdir}/pkgconfig/source-highlight.pc
%{_includedir}/srchilite/*.h

%changelog
* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 3.1.8-2
- Initial build

