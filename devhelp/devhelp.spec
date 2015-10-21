
Name: devhelp
Version: 3.16.1
Release: 4 
License: GPLv2+
Group: Development/Tools
Summary: API document browser
URL: http://www.gnome.org
Source: http://download.gnome.org/sources/devhelp/%{version}/devhelp-%{version}.tar.xz

Requires: webkitgtk

BuildRequires: desktop-file-utils >= 0.3
BuildRequires: webkitgtk-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gtk3-devel

%description
An API document browser

%package devel
Summary: Library to embed Devhelp in other applications.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk3-devel >= %{gtk3_version}
Requires: pkgconfig

%description devel
Library of Devhelp for embedding into other applications

%prep
%setup -q
%build
%configure --disable-static --disable-schemas-compile
make %{?_smp_mflags}

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/
install -m 0644 misc/devhelp.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/

%find_lang devhelp
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  gtk3-update-icon-cache -q %{_datadir}/icons/hicolor
fi
glib-compile-schemas /usr/share/glib-2.0/schemas >/dev/null 2>&1 || :

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk3-update-icon-cache ]; then
  gtk3-update-icon-cache -q %{_datadir}/icons/hicolor
fi
glib-compile-schemas /usr/share/glib-2.0/schemas >/dev/null 2>&1 || :

%files -f devhelp.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README 

%{_bindir}/devhelp
%{_libdir}/libdevhelp*.so.*

%{_datadir}/applications/*.desktop
%{_datadir}/devhelp
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor
%{_datadir}/emacs/site-lisp/site-start.d/devhelp.el
%{_libdir}/gedit/plugins/*
%{_datadir}/GConf/gsettings/devhelp.convert
%{_datadir}/appdata/devhelp.appdata.xml

%files devel
%defattr(-,root,root)
%{_prefix}/include/devhelp-*
%{_libdir}/libdevhelp*.so
%{_libdir}/pkgconfig/*

%changelog
