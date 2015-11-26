%define rel 1_10_8
Name: workrave
Version: 1.10
Release: 2%{?dist}
Summary: Program that assists in the recovery and prevention of RSI
License: GPLv3+
Group: Applications/Productivity
URL: http://www.workrave.org/
# https://github.com/rcaelers/workrave
Source0: workrave-%{rel}.tar.gz

BuildRequires: glib2-devel >= 2.28.0
BuildRequires: gtk3-devel >= 3.0.0
BuildRequires: libsigc++-devel >= 2.2.4.2
BuildRequires: glibmm-devel >= 2.28.0
BuildRequires: gtkmm-devel >= 3.0.0
BuildRequires: gobject-introspection-devel
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: libXmu-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: dbus-devel
BuildRequires: gstreamer-devel
BuildRequires: intltool
BuildRequires: python-cheetah
BuildRequires: pulseaudio-libs-devel
BuildRequires: autoconf, automake, libtool

Requires: dbus

%description
Workrave is a program that assists in the recovery and prevention of
Repetitive Strain Injury (RSI). The program frequently alerts you to
take micro-pauses, rest breaks and restricts you to your daily limit.

%package devel
Requires: %{name} = %{version}-%{release}
Summary: Development files for workrave

%description devel
Development files for workrave.

%prep
%setup -q -n %{name}-%{rel}
sed -i 's/AX_CXX_COMPILE_STDCXX_11/MM_AX_CXX_COMPILE_STDCXX_11/g' configure.ac
touch ChangeLog

%build
export CXXFLAGS="-std=c++11"
if [ ! -x configure ]; then
  ### Needed for snapshot releases.
  NOCONFIGURE=1 ./autogen.sh
fi

%configure \
    --disable-gnome2 \
    --disable-static \
    --disable-xml \
    --disable-dbus \
    --disable-gsettings \
    --disable-gnome3 \
    --disable-indicator \
    --enable-gconf

make V=1

%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a

%find_lang %{name}

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_datadir}/workrave/
%{_datadir}/sounds/workrave/
%{_datadir}/icons/hicolor/16x16/apps/workrave.png
%{_datadir}/icons/hicolor/24x24/apps/workrave.png
%{_datadir}/icons/hicolor/32x32/apps/workrave.png
%{_datadir}/icons/hicolor/48x48/apps/workrave.png
%{_datadir}/icons/hicolor/64x64/apps/workrave.png
%{_datadir}/icons/hicolor/96x96/apps/workrave.png
%{_datadir}/icons/hicolor/128x128/apps/workrave.png
%{_datadir}/icons/hicolor/scalable/workrave-sheep.svg
%{_datadir}/icons/hicolor/scalable/apps/workrave.svg
%{_datadir}/applications/workrave.desktop
%{_datadir}/appdata/workrave.appdata.xml
%{_datadir}/gnome-shell/extensions/workrave@workrave.org/
%{_libdir}/girepository-1.0/Workrave-1.0.typelib
%{_libdir}/libworkrave-private-1.0.so.*

%files devel
%{_datadir}/gir-1.0/Workrave-1.0.gir
%{_libdir}/libworkrave-private-1.0.so

%changelog
* Thu Nov 26 2015 Cjacker <cjacker@foxmail.com> - 1.10-2
- Initial build

