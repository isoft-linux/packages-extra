Name: audacious 
Version: 3.7
Release: 4.b1 
Summary: An Advanced Audio Player

License: See license in source 
URL: http://audacious-media-player.org/
Source0: http://distfiles.audacious-media-player.org/%{name}-%{version}-beta1.tar.bz2
Patch0: audacious-set-chardet-fallback-to-gbk.patch

BuildRequires: qt5-qtbase-devel 
# for /usr/bin/appstream-util
BuildRequires: appstream-glib

BuildRequires: gettext
BuildRequires: pkgconfig(libguess)
BuildRequires: desktop-file-utils
BuildRequires: glib2-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)

# without plugins, fail to run audacious
Requires: audacious-plugins

%description
Audacious is an open source audio player. 

%package libs 
Summary: Runtime libraries of %{name}

%description libs 
The %{name}-libs package contains runtime libraries of %{name}.

%package devel
Summary: Development files of %{name}
Requires: %{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications and %{name} plugins that use %{name}-libs.

%prep
%setup -q -n %{name}-%{version}-beta1
%patch0 -p1

%build
%configure \
 --disable-gtk \
 --enable-qt
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

install -D -m0644 contrib/%{name}.appdata.xml ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{name}.appdata.xml

#own this folder 
mkdir -p %{buildroot}%{_libdir}/audacious

%find_lang audacious

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi
update-desktop-database -q &> /dev/null ||:
fi

%files -f audacious.lang
%{_bindir}/audacious
%{_bindir}/audtool

%{_datadir}/audacious
#own this folder
%{_libdir}/audacious

%{_datadir}/applications/audacious.desktop
%{_datadir}/icons/hicolor/*/apps/audacious.*
%{_datadir}/appdata/audacious.appdata.xml
%{_mandir}/man1/audacious.1.gz
%{_mandir}/man1/audtool.1.gz

%files libs
%{_libdir}/libaud*.so.*

%files devel
%{_includedir}/audacious
%{_includedir}/libaudcore
%{_includedir}/libaudqt
%{_libdir}/libaud*.so
%{_libdir}/pkgconfig/audacious.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.7-4.b1
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 3.7-3.b1
- Update to 3.7beta1



