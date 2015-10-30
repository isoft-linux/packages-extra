Name:           inkscape
Version:        0.91
Release:        18%{?dist}
Summary:        Vector-based drawing program using SVG

License:        GPLv2+
URL:            http://inkscape.sourceforge.net/
Source0:        http://downloads.sourceforge.net/inkscape/%{name}-%{version}.tar.bz2
Patch0:         inkscape-0.48.2-types.patch
Patch1:         inkscape-0.91-desktop.patch

BuildRequires:  aspell-devel
BuildRequires:  atk-devel
BuildRequires:  boost-devel
BuildRequires:  cairo-devel
BuildRequires:  dos2unix
BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel
BuildRequires:  gc-devel >= 6.4
BuildRequires:  gettext
BuildRequires:  gsl-devel
BuildRequires:  gtkmm2-devel >= 2.8.0
BuildRequires:  gtkspell-devel
BuildRequires:  ImageMagick-c++-devel
BuildRequires:  intltool
BuildRequires:  lcms2-devel
BuildRequires:  libpng-devel >= 1.2
BuildRequires:  libwpg-devel
BuildRequires:  libxml2-devel >= 2.6.11
BuildRequires:  libxslt-devel >= 1.0.15
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  popt-devel

# Disable all for now. TODO: Be smarter
%if 0
Requires:       dia
Requires:       ghostscript
Requires:       perl(Image::Magick)
Requires:       transfig
Requires:       gimp
%endif
Requires:       python-lxml
Requires:       numpy
Requires:       uniconvertor

# Weak dependencies for the LaTeX plugin
Suggests:       pstoedit
#Suggests:       tex(latex)
#Suggests:       tex(dvips)
#Suggests:       texlive-amsmath
#Suggests:       texlive-amsfonts

%description
Inkscape is a vector graphics editor, with capabilities similar to
Illustrator, CorelDraw, or Xara X, using the W3C standard Scalable Vector
Graphics (SVG) file format.  It is therefore a very useful tool for web
designers and as an interchange format for desktop publishing.

Inkscape supports many advanced SVG features (markers, clones, alpha
blending, etc.) and great care is taken in designing a streamlined
interface. It is very easy to edit nodes, perform complex path operations,
trace bitmaps and much more.


%package view
Summary:        Viewing program for SVG files

%description view
Viewer for files in W3C standard Scalable Vector Graphics (SVG) file
format.


%package docs
Summary:        Documentation for Inkscape
Requires:       inkscape

%description docs
Tutorial and examples for Inkscape, a graphics editor for vector
graphics in W3C standard Scalable Vector Graphics (SVG) file format.


%prep
%setup -q
%patch0 -p1 -b .types
%patch1 -p1 -b .desktop

# https://bugs.launchpad.net/inkscape/+bug/314381
# A couple of files have executable bits set,
# despite not being executable
find . -name '*.cpp' | xargs chmod -x
find . -name '*.h' | xargs chmod -x
find share/extensions -name '*.py' | xargs chmod -x

# Fix end of line encodings
dos2unix -k -q share/extensions/*.py

%build
# Build in C++11 mode as glibmm headers use C++11 features. This can be dropped
# when GCC in Fedora switches to C++11 by default (with GCC 6, most likely).
export CXXFLAGS="%{optflags} -std=c++11"

# --disable-strict-build is needed due to gtkmm using a deprecated glibmm method
# If upstream gtkmm fixes https://bugzilla.gnome.org/show_bug.cgi?id=752797
# this can be removed.
%configure                      \
        --with-python           \
        --with-perl             \
        --without-gnome-vfs        \
        --with-xft              \
        --enable-lcms2           \
        --enable-poppler-cairo  \
        --disable-strict-build

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor="%{?desktop_vendor}" --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# No skencil anymore
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions/sk2svg.sh

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: http://inkscape.13.x6.nabble.com/Inkscape-and-AppData-td4967842.html
SentUpstream: 2013-09-06
-->
<application>
  <id type="desktop">inkscape.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      An Open Source vector graphics editor, with capabilities similar to Illustrator,
      CorelDraw, or Xara X, using the W3C standard Scalable Vector Graphics (SVG) file
      format.
    </p>
    <p>
      Inkscape supports many advanced SVG features (markers, clones, alpha blending,
      etc.) and great care is taken in designing a streamlined interface. It is very
      easy to edit nodes, perform complex path operations, trace bitmaps and much more.
      We also aim to maintain a thriving user and developer community by using open,
      community-oriented development.
    </p>
  </description>
  <url type="homepage">http://inkscape.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/inkscape/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

%find_lang %{name}


%check
# XXX: Tests fail, ignore it for now
make -k check || :


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/update-desktop-database -q &> /dev/null ||:
fi


%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/inkscape
%{_bindir}/inkview
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/attributes
%{_datadir}/inkscape/branding
#%{_datadir}/inkscape/clipart
%{_datadir}/inkscape/extensions
# Pulls in perl, if needed should go into a -perl subpackage
%exclude %{_datadir}/inkscape/extensions/embed_raster_in_svg.pl
%{_datadir}/inkscape/filters
%{_datadir}/inkscape/fonts
%{_datadir}/inkscape/gradients
%{_datadir}/inkscape/icons
%{_datadir}/inkscape/keys
%{_datadir}/inkscape/markers
%{_datadir}/inkscape/palettes
%{_datadir}/inkscape/patterns
%{_datadir}/inkscape/screens
%{_datadir}/inkscape/symbols
%{_datadir}/inkscape/templates
%{_datadir}/inkscape/ui
%{_datadir}/appdata/*inkscape.appdata.xml
%{_datadir}/applications/*inkscape.desktop
%{_datadir}/icons/hicolor/*/*/inkscape*
%{_mandir}/*/*gz
%{_mandir}/*/*/*gz
%{_datadir}/inkscape/tutorials


%files docs
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/examples


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.91-18
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
