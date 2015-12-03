%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           notify-python
Version:        0.1.1
Release:        30%{?dist}
Summary:        Python bindings for libnotify

Group:          Development/Languages
# No version specified, just COPYING.
License:        LGPLv2+
URL:            http://www.galago-project.org
Source0:        http://www.galago-project.org/files/releases/source/notify-python/notify-python-%{version}.tar.bz2
Patch0:         notify-python-0.1.1-fix-GTK-symbols.patch
Patch1:         libnotify07.patch

BuildRequires:  python-devel, pkgconfig
BuildRequires:  libnotify-devel >= 0.7.0
BuildRequires:  pygtk2-devel
BuildRequires:  gtk2-devel, dbus-devel, dbus-glib-devel
BuildRequires:  autoconf

Requires:   libnotify >= 0.4.3
Requires:   desktop-notification-daemon
Requires:   pygtk2

%global pypkgname pynotify

%description
Python bindings for libnotify

%prep
%setup -q
%patch0 -p1 -b .fix-GTK-symbols
%patch1 -p1 -b .libnotify07

# WARNING - we touch src/pynotify.override in build because upstream did not rebuild pynotify.c
# from the input definitions, this forces pynotify.c to be regenerated, at some point this can be removed

%build
export PYTHON=%{__python}
autoconf

%configure
touch src/pynotify.override
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# remove unnecessary la file
rm $RPM_BUILD_ROOT/%{python_sitearch}/gtk-2.0/%{pypkgname}/_%{pypkgname}.la
mkdir -p examples
install -m 0644 -t examples tests/*.py tests/*.png

 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS ChangeLog
%doc examples
%{python_sitearch}/gtk-2.0/%{pypkgname}
%{_datadir}/pygtk/2.0/defs/%{pypkgname}.defs
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.1.1-30
- Init for isoft4

