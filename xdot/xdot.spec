Name:   xdot 
Version: 0.6
Release: 2
Summary: xdot is an interactive viewer for graphs written in Graphviz's dot language.
License: GPLv2+
URL:     https://github.com/jrfonseca/xdot.py
Source0: %{name}-%{version}.tar.gz
Source1: xdot.desktop
Patch0:  xdot-gv-filter.patch
Patch1:  xdot-fix-start-from-menu.patch

BuildArch: noarch

Requires: python, pygtk2

%description
xdot is an interactive viewer for graphs written in Graphviz's dot language.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%build

%install
install -D -m0755 xdot.py $RPM_BUILD_ROOT%{_bindir}/xdot
install -D -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications/xdot.desktop
%check

%post
update-desktop-database -q ||:
%postun
update-desktop-database -q ||:

%clean
rm -rf $RPM_BUILD_ROOT
%files
%{_bindir}/xdot
%{_datadir}/applications/xdot.desktop
%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.6-2
- Rebuild

