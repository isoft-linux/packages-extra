%global archive_version 20150612
%global gettext_package FontForge
%global gnulib_githead 2bf7326

Name:           fontforge
Version:        20150612
Release:        3
Summary:        Outline and bitmap font editor

License:        GPLv3+
URL:            http://fontforge.github.io/
Source0:        https://github.com/fontforge/fontforge/archive/%{archive_version}.tar.gz
# https://github.com/fontforge/fontforge/issues/1725
Source1:        http://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=snapshot;h=%{gnulib_githead};sf=tgz;name=gnulib-%{gnulib_githead}.tar.gz
# https://github.com/fontforge/fontforge/pull/1723
Patch0:         fontforge-20140813-use-system-uthash.patch

Requires:       xdg-utils
Requires:       autotrace
Requires:       hicolor-icon-theme

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  libungif-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libuninameslist-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  gettext
BuildRequires:  pango-devel
BuildRequires:  cairo-devel
BuildRequires:  libspiro-devel
BuildRequires:  python-devel
BuildRequires:  libltdl-devel
BuildRequires:  readline-devel
# This is failing on aarch64 so drop it
#BuildRequires:  python-ipython
BuildRequires:  uthash-devel

%description
FontForge (former PfaEdit) is a font editor for outline and bitmap
fonts. It supports a range of font formats, including PostScript
(ASCII and binary Type 1, some Type 3 and Type 0), TrueType, OpenType
(Type2) and CID-keyed fonts.

%package devel
Summary: Development tools for fontforge
Requires: %{name} = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes the libraries and header files you will need
to compile applications against fontforge.

%package doc
Summary: Documentation files for %{name}
BuildArch: noarch

%description doc
This package contains documentation files for %{name}.


%prep
%setup -q -n %{name}-%{archive_version}
tar xzf %{SOURCE1}

%patch0 -p0

sed -i -e '/^#!\//, 1d' pycontrib/graphicore.py
sed -i -e '/^#!\//, 1d' pycontrib/webcollab.py

mkdir htdocs
cp -pr doc/html/* htdocs
chmod 644 htdocs/nonBMP/index.html
# Fix bad line terminators
%{__sed} -i 's/\r//' htdocs/Big5.txt
%{__sed} -i 's/\r//' htdocs/corpchar.txt

%build
./bootstrap --skip-git --gnulib-srcdir=gnulib-%{gnulib_githead}
export CFLAGS="%{optflags} -fno-strict-aliasing"

%configure
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/libg{draw,unicode}.{la,so}


# The fontforge makefiles install htdocs as well, but we
# prefer to have them under the standard RPM location, so
# remove the extra copy
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/fontforge

# remove unneeded .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

# Find translations
%find_lang %{gettext_package}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
install -m 644 -p desktop/fontforge.appdata.xml $RPM_BUILD_ROOT%{_datadir}/appdata

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages
install -m 644 -p desktop/fontforge.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/

#Makefile install rules are playing evil here. Let's correct the permission.
#chmod 644 $RPM_BUILD_ROOT%{_datadir}/fontforge/python/graphicore/__init__.py
chmod 644 $RPM_BUILD_ROOT%{_datadir}/fontforge/python/gdraw/_gdraw.py

chmod 644 $RPM_BUILD_ROOT%{_datadir}/fontforge/nodejs/collabwebview/css/*.css
chmod 644 $RPM_BUILD_ROOT%{_datadir}/fontforge/nodejs/collabwebview/js/*.js
chmod 644 $RPM_BUILD_ROOT%{_datadir}/fontforge/nodejs/collabwebview/js/contentEditable/*

%post
update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/sbin/ldconfig

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
/sbin/ldconfig

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{gettext_package}.lang
%doc AUTHORS
%license LICENSE
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/applications/*fontforge.desktop
%{_datadir}/fontforge
%{_datadir}/icons/hicolor/*/apps/fontforge.*
%{_mandir}/man1/*.1*
%{_datadir}/mime/packages/fontforge.xml
%{_datadir}/appdata/fontforge.appdata.xml
%{python_sitearch}/fontforge.so
%{python_sitearch}/psMat.so

%files devel
%{_includedir}/fontforge/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc htdocs

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 20150612-3
- Rebuild

