Name:      brasero
Version:   3.12.1
Release:   4%{?dist}
Summary:   Gnome CD/DVD burning application
# see https://bugzilla.gnome.org/show_bug.cgi?id=683503
License:   GPLv3+
URL:       http://www.gnome.org/projects/brasero/
#VCS: git:git://git.gnome.org/brasero
Source0:   http://ftp.gnome.org/pub/GNOME/sources/brasero/3.12/%{name}-%{version}.tar.gz

Patch0:         brasero-libdvdcss.patch

BuildRequires:  gtk3-devel >= 2.99.0
BuildRequires:  glib2-devel >= 2.15.6
BuildRequires:  gettext intltool gtk-doc
BuildRequires:  desktop-file-utils
BuildRequires:  gstreamer-devel >= 0.11.92
BuildRequires:  gstreamer-plugins-base-devel >= 0.11.92
BuildRequires:  totem-pl-parser-devel >= 2.22.0
BuildRequires:  libnotify-devel >= 0.7.0
BuildRequires:  libxml2-devel >= 2.6.0
BuildRequires:  dbus-glib-devel >= 0.7.2
BuildRequires:  libxslt
BuildRequires:  libappstream-glib
BuildRequires:  libburn-devel >= 0.4.0
BuildRequires:  libisofs-devel >= 0.6.4
BuildRequires:  nautilus-devel >= 2.22.2
BuildRequires:  libSM-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libcanberra-gtk3-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  tracker-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  gnome-common
BuildRequires:  itstool
BuildRequires:  yelp-tools

Requires:  dvd+rw-tools
#Requires:  cdrecord
#Requires:  mkisofs
#Requires:  cdda2wav
# the up 3 items is provided by cdrkit now.
Requires:  cdrkit
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}
%ifnarch s390 s390x
Requires:  cdrdao
%endif

%description
Simple and easy to use CD/DVD burning application for the Gnome
desktop.


%package   libs
Summary:   Libraries for %{name}
Group:     System Environment/Libraries
Obsoletes: nautilus-cd-burner-libs < 2.25.4


%description libs
The %{name}-libs package contains the runtime shared libraries for
%{name}.


%package   nautilus
Summary:   Nautilus extension for %{name}
Group:     User Interface/Desktops

Provides:  nautilus-cd-burner = %{version}-%{release}
Obsoletes: nautilus-cd-burner < 2.25.4
Requires:  %{name} = %{version}-%{release}

%description nautilus
The %{name}-nautilus package contains the brasero nautilus extension.


%package        devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      nautilus-cd-burner-devel < 2.25.4


%description devel
This package contains the static libraries and header files needed for
developing brasero applications.


%prep
%setup -q
%patch0 -p1


%build
%configure \
        --enable-nautilus \
        --enable-libburnia \
        --enable-search \
        --enable-playlist \
        --enable-preview \
        --enable-inotify \
        --disable-caches \
        --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%find_lang %{name}

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/brasero.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/b.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/c.png 

sed -i 's/cd:x/cd;x/' $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor ""                   \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications  \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor ""                   \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications  \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-nautilus.desktop


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml


%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null ||:


%post libs -p /sbin/ldconfig


%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{_datadir}/mime &> /dev/null || :
fi


%postun libs -p /sbin/ldconfig


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%{!?_licensedir:%global license %doc}
%license COPYING
%doc AUTHORS NEWS README
%{_mandir}/man1/%{name}.*
%{_bindir}/*
%{_libdir}/brasero3
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/help/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/*
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml

%files libs
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files nautilus
%{_libdir}/nautilus/extensions-3.0/*.so
%{_datadir}/applications/brasero-nautilus.desktop


%files devel
%doc %{_datadir}/gtk-doc/html/libbrasero-media
%doc %{_datadir}/gtk-doc/html/libbrasero-burn
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/brasero3
%{_datadir}/gir-1.0/*.gir


%changelog
* Tue Mar 22 2016 sulit <sulitsrc@gmail.com> - 3.12.1-4
- Init for isoft5
- add libcanberra-gtk3-devel buildrequire

