Name:           mono-debugger
Summary:        Mono Debugger
License:        GPL-2.0+ and LGPL-2.0+ and MIT
Url:            http://www.mono-project.com/Debugger
Version:        2.10
Release:        53.6
Source:         http://download.mono-project.com/sources/mono-debugger/%{name}-%{version}.tar.bz2
Source99:       mono-debugger-rpmlintrc
Patch1:         mono-debugger-glib.patch
ExclusiveArch:  %ix86 x86_64
BuildRequires:  glib2-devel
BuildRequires:  mono-devel
#for mono-nunit
BuildRequires:  mono
BuildRequires:  ncurses-devel

%description
A debugger is an important tool for development. The Mono Debugger
(MDB) can debug both managed and unmanaged applications.  It provides a
reusable library that can be used to add debugger functionality to
different front-ends. The debugger package includes a console debugger
named "mdb", and MonoDevelop (http://www.monodevelop.com) provides a
GUI interface to the debugger.

%prep
%setup -q
%patch1 -p1

%build
mcsver=`mcs --version | cut -d" " -f5 | cut -d"." -f1`
if [ "$mcsver" -ge "4" ]; then
  export MCS="/usr/bin/mcs"
fi
%configure
make

%install
make install DESTDIR=%{buildroot}
# Unset executable bit on .exe files
# This prevents the dbuginfo macros from scanning them
find %{buildroot} -name '*.exe' -exec chmod a-x '{}' ';'
find %{buildroot} -name '*.dll' -exec chmod a-x '{}' ';'
# Remove unnecessary devel files
rm -f %{buildroot}%_libdir/*.la
rm -f %{buildroot}%_libdir/*.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README NEWS
%{_bindir}/mdb*
%{_libdir}/*.so*
%{_prefix}/lib/mono/2.0/mdb*.exe
%{_prefix}/lib/mono/gac/Mono.Debugger*
%{_prefix}/lib/mono/mono-debugger
%{_libdir}/pkgconfig/mono-debugger*.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.10-53.6
- Rebuild

