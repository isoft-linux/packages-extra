Name: gtkspell
Version: 2.0.16
Release: 11%{?dist}
License: GPLv2+
Summary: On-the-fly spell checking for GtkTextView widgets
URL: http://gtkspell.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Source: http://gtkspell.sourceforge.net/download/%{name}-%{version}.tar.gz

### Build Dependencies ###

BuildRequires: enchant-devel
BuildRequires: gtk2-devel
BuildRequires: gettext
BuildRequires: intltool

%description
GtkSpell provides word-processor-style highlighting and replacement of 
misspelled words in a GtkTextView widget as you type. Right-clicking a
misspelled word pops up a menu of suggested replacements.

%package devel
Summary: Development files for GtkSpell
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel
Requires: pkgconfig

%description devel
The gtkspell-devel package provides header files for developing 
applications which use GtkSpell.

%prep
%setup -q

%build
%configure --disable-gtk-doc --disable-static 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING
%{_libdir}/libgtkspell.so.0*

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/gtkspell
%{_includedir}/gtkspell-2.0
%{_libdir}/libgtkspell.so
%{_libdir}/pkgconfig/gtkspell-2.0.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0.16-11
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
