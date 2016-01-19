Name:           highlight

Summary:        Universal source code to formatted text converter

Version:        3.22
Release:        5%{?dist}
License:        GPLv3

URL:            http://www.andre-simon.de/
Source0:        http://www.andre-simon.de/zip/%{name}-%{version}.tar.bz2

BuildRequires:  qt4-devel
BuildRequires:  lua-devel, boost-devel
# Only required for 3.16.1
BuildRequires:  desktop-file-utils

%{?filter_setup:
%filter_from_provides /^perl(/d;
%filter_from_requires /^perl(/d;
%filter_setup
}

%description
A utility that converts sourcecode to HTML, XHTML, RTF, LaTeX, TeX,
XSL-FO, XML or ANSI escape sequences with syntax highlighting.
It supports several programming and markup languages.
Language descriptions are configurable and support regular expressions.
The utility offers indentation and reformatting capabilities.
It is easily possible to create new language definitions and colour themes.

# %package gui
# Summary:        GUI for the hihghlight source code formatter
# Requires:       %{name} = %{version}-%{release}
#
# %description gui
# A Qt-based GUI for the highlight source code formatter source.

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=
rm -rf src/gui-qt/moc*
#make gui %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"  \
#                         QMAKE="qmake-qt4" \
#                         LDFLAGS=

%install
make install DESTDIR=$RPM_BUILD_ROOT

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps

#make install-gui DESTDIR=$RPM_BUILD_ROOT

#rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/

#desktop-file-install \
#    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
#   highlight.desktop

%files
%defattr(-,root,root,-)
%{_bindir}/highlight
%{_datadir}/highlight/
%{_mandir}/man1/highlight.1*

%config(noreplace) %{_sysconfdir}/highlight/

%doc ChangeLog AUTHORS README* COPYING TODO examples/

# %files gui
# %defattr(-,root,root,-)
# %{_bindir}/highlight-gui
# %{_datadir}/applications/highlight.desktop
# %{_datadir}/pixmaps/highlight.xpm

%changelog
* Tue Jan 19 2016 sulit <sulitsrc@gmail.com> - 3.22-5
- Init for isoft4, and remove gui for it's bad

