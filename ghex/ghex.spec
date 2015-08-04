Name:           ghex
Version:        3.10.1
Release:        1
Summary:        Binary editor for GNOME

Group:          Applications/Editors
License:        GPLv2+
URL:            http://ftp.gnome.org/pub/GNOME/sources/ghex/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/ghex/3.10/ghex-%{version}.tar.xz

BuildRequires:  gtk3-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  itstool
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
GHex can load raw data from binary files and display them for editing in the
traditional hex editor view. The display is split in two columns, with
hexadecimal values in one column and the ASCII representation in the other.
A useful tool for working with raw data.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
export CC=clang
export CXX=clang++

%configure --enable-compile-warnings=no
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT DATADIRNAME=share

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ghex.desktop

%find_lang %{name}-3.0 --all-name --with-gnome

rpmclean

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk3-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

    touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :
    gtk3-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk3-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk3-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :


%files -f %{name}-3.0.lang
%doc AUTHORS COPYING COPYING-DOCS HACKING NEWS README
%{_bindir}/*
%{_datadir}/appdata/ghex.appdata.xml
%{_datadir}/applications/ghex.desktop
%{_datadir}/GConf/gsettings/ghex.convert
%{_datadir}/glib-2.0/schemas/org.gnome.GHex.gschema.xml
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/HighContrast/*/apps/ghex.png
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
