Summary: EFL toolkit for small touchscreens
Name: elementary
Version: 1.15.2
Release: 3 
License: Lesser GPL
URL: http://trac.enlightenment.org/e/wiki/Elementary
Source: http://download.enlightenment.org/rel/libs/elementary/%{name}-%{version}.tar.gz
Patch0: elementary-add-adwaita-icon-theme.patch

BuildRequires: efl-devel
#for convert
BuildRequires: ImageMagick
%description
Elementary is a widget set. It is a new-style of widget set much more canvas
object based than anything else. Why not ETK? Why not EWL? Well they both
tend to veer away from the core of Evas, Ecore and Edje a lot to build their
own worlds. Also I wanted something focused on embedded devices -
specifically small touchscreens. Unlike GTK+ and Qt, 75% of the "widget set"
is already embodied in a common core - Ecore, Edje, Evas etc. So this
fine-grained library splitting means all of this is shared, just a new
widget "personality" is on top. And that is... Elementary, my dear watson.
Elementary.


%package devel
Summary: Elementary headers, static libraries, documentation and test programs
Requires: %{name} = %{version}
Requires: efl-devel

%description devel
Headers, static libraries, test programs and documentation for Elementary

%package doc
Summary: EFL API documents
Requires: %{name} = %{version}
Requires: efl-doc 

%description doc
EFL API documents.

%prep
%setup -q
%patch0 -p1


%build
export CC=clang
export CXX=clang++
%configure

make %{?_smp_mflags}
make doc %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/elementary/html
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/elementary/examples
cp -r doc/html/* $RPM_BUILD_ROOT/usr/share/doc/elementary/html
cp -r src/examples/*.c $RPM_BUILD_ROOT/usr/share/doc/elementary/examples
cp -r src/examples/*.edc $RPM_BUILD_ROOT/usr/share/doc/elementary/examples

%find_lang %{name}

%post
/sbin/ldconfig || :


%postun
/sbin/ldconfig || :


%clean
test "x$RPM_BUILD_ROOT" != "x/" && rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/edje/*
%{_libdir}/elementary/
%{_datadir}/applications/*
%{_datadir}/icons/*
%{_datadir}/elementary/*


#%doc AUTHORS COPYING README
#%{_libdir}/*.a
#%{_libdir}/*.la
#%{_libdir}/*.so
#%{_libdir}/libelementary*.so.*
#%{_libdir}/edje/modules/elm/
#
%files devel
%defattr(-, root, root)
%{_libdir}/*.so
#%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/*
%{_docdir}/elementary
%dir %{_datadir}/eolian
%{_datadir}/eolian/*

%files doc
%doc doc/html

#
#%files bin
#%defattr(-, root, root)
#%{_bindir}/*
#%{_datadir}/applications/*.desktop
#%{_datadir}/elementary/
#%{_datadir}/icons/elementary.png
#
#
%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.15.2-3
- Rebuild

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 1.15.2
* Tue Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update to 1.15.0

