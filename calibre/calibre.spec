%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%global __provides_exclude_from ^%{_libdir}/%{name}/%{name}/plugins/.*\.so$

Name:           calibre
Version:        2.42.0
Release:        1%{?dist}
Summary:        E-book converter and library manager
License:        GPLv3
URL:            http://calibre-ebook.com/

# SourceURL: curl -L http://code.calibre-ebook.com/dist/src > calibre-%%{version}.tar.xz
# Upstream packages some unfree fonts which we cannot redistribute.
# While we're at it, also delete the liberation fonts which we already have.
#
# Download the upstream tarball and invoke this script while in the tarball's
# directory:
# ./generate-tarball.sh %%{version}

Source0:        %{name}-%{version}-nofonts.tar.xz
Source1:        generate-tarball.sh
Source2:        calibre-mount-helper
Source3:        calibre-gui.appdata.xml
#
# Disable auto update from inside the app
#
Patch1:         %{name}-no-update.patch
#
# Do not display multiple apps in desktop files, only the main app
# This is so gnome-software only 'sees' calibre once. 
# 
Patch3:         calibre-nodisplay.patch

BuildRequires:  python >= 2.6
BuildRequires:  python-devel >= 2.6
BuildRequires:  ImageMagick-devel
BuildRequires:  python-setuptools
BuildRequires:  python-qt5-devel
BuildRequires:  python-qt5
BuildRequires:  podofo-devel
BuildRequires:  desktop-file-utils
BuildRequires:  python-mechanize
BuildRequires:  python-lxml
BuildRequires:  python-dateutil
BuildRequires:  python-imaging
BuildRequires:  xdg-utils
BuildRequires:  python-BeautifulSoup
BuildRequires:  chmlib-devel
BuildRequires:  python-cssutils >= 0.9.9
BuildRequires:  sqlite-devel
BuildRequires:  libicu-devel
BuildRequires:  libpng-devel
BuildRequires:  libmtp-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  web-assets-devel
BuildRequires:  libXrender-devel
BuildRequires:  systemd-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  openssl-devel
# calibre installer is so smart that it check for the presence of the
# directory (and then installs in the wrong place)
BuildRequires:  bash-completion
BuildRequires:  python-apsw
BuildRequires:  glib2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libinput-devel
BuildRequires:  libxkbcommon-devel
#
# If python-feedparser is installed at build time there's problems with links. 
# See https://bugzilla.redhat.com/show_bug.cgi?id=1026469
BuildConflicts: python-feedparser

%{?pyqt5_requires}
# once ^^ %%pyqt5_requires is everywhere, can drop python-qt5 dep below -- rex

# Add hard dep to specific qtbase pkg, see build message below -- rex
# Project MESSAGE: This project is using private headers and will therefore be tied to this specific Qt module build version.
# Project MESSAGE: Running this project against other versions of the Qt modules may crash at any arbitrary point.
# Project MESSAGE: This is not a bug, but a result of using Qt internals. You have been warned!
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

Requires:       python-qt5
Requires:       qt5-qtwebkit
Requires:       qt5-qtsvg
Requires:       python-cherrypy
Requires:       python-cssutils
Requires:       ImageMagick
Requires:       odfpy
Requires:       python-lxml
Requires:       python-imaging
Requires:       python-mechanize
Requires:       python-dateutil
Requires:       python-genshi
Requires:       python-BeautifulSoup
Requires:       poppler-utils
Requires:       fonts-liberation
# Require the packages of the files which are symlinked by calibre
Requires:       python-feedparser
Requires:       python-netifaces
Requires:       python-dns
Requires:       python-cssselect
Requires:       python-apsw
Requires:       mathjax

%description
Calibre is meant to be a complete e-library solution. It includes library
management, format conversion, news feeds to ebook conversion as well as
e-book reader sync features.

Calibre is primarily a ebook cataloging program. It manages your ebook
collection for you. It is designed around the concept of the logical book,
i.e. a single entry in the database that may correspond to ebooks in several
formats. It also supports conversion to and from a dozen different ebook
formats.

Supported input formats are: MOBI, LIT, PRC, EPUB, CHM, ODT, HTML, CBR, CBZ,
RTF, TXT, PDF and LRS.

%prep
%setup -q -n %{name}-%{version}

# don't check for new upstream version (that's what packagers do)
%patch1 -p1 -b .no-update
# Hide individual launchers for ebook-edit, ebook-viewer and lrfviewer as they
# are all accessible in the main calibre GUI.
%patch3 -p1 -b .nodisplay

# dos2unix newline conversion
sed -i 's/\r//' src/calibre/web/feeds/recipes/*

# remove shebangs
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*.py
sed -i -e '/^#![ ]*\//, 1d' src/calibre/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*.py
sed -i -e '/^#!\//, 1d' src/templite/*.py
sed -i -e '/^#!\//, 1d' resources/default_tweaks.py
sed -i -e '/^#!\//, 1d' resources/catalog/section_list_templates.py

chmod -x src/calibre/*/*/*/*.py \
    src/calibre/*/*/*.py \
    src/calibre/*/*.py \
    src/calibre/*.py

rm -rvf resources/viewer/mathjax

%build
OVERRIDE_CFLAGS="%{optflags}" python setup.py build

%install
mkdir -p %{buildroot}%{_datadir}

# create directories for xdg-utils
mkdir -p %{buildroot}%{_datadir}/icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor
mkdir -p %{buildroot}%{_datadir}/packages
mkdir -p %{buildroot}%{_datadir}/mime
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/desktop-directories

# create directory for gnome software data
mkdir -p %{buildroot}%{_datadir}/appdata

# create directory for calibre environment module
# the install script assumes it's there.
mkdir -p %{buildroot}%{python_sitelib}

# create directory for completion files, so calibre knows where
# to install them
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

XDG_DATA_DIRS="%{buildroot}%{_datadir}" \
XDG_UTILS_INSTALL_MODE="system" \
LIBPATH="%{_libdir}" \
python setup.py install --root=%{buildroot}%{_prefix} \
                        --prefix=%{_prefix} \
                        --libdir=%{_libdir} \
                        --staging-libdir=%{buildroot}%{_libdir} \
                        --staging-sharedir=%{buildroot}%{_datadir}

# remove shebang from init_calibre.py here because
# it just got spawned by the install script
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/init_calibre.py

# icons
mkdir -p %{buildroot}%{_datadir}/pixmaps/
cp -p resources/images/library.png                \
   %{buildroot}%{_datadir}/pixmaps/%{name}-gui.png
cp -p resources/images/viewer.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-viewer.png
cp -p resources/images/tweak.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-ebook-edit.png

# every file is empty here
find %{buildroot}%{_datadir}/mime -maxdepth 1 -type f -print -delete

# packages aren't allowed to register mimetypes like this
rm -f %{buildroot}%{_datadir}/applications/defaults.list
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache
rm -f %{buildroot}%{_datadir}/mime/application/*.xml
rm -f %{buildroot}%{_datadir}/mime/text/*.xml

desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-ebook-viewer.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-gui.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-lrfviewer.desktop

# mimetype icon for lrf
rm -rf %{buildroot}%{_datadir}/icons/hicolor/128x128
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -p resources/images/mimetypes/lrf.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-sony-bbeb.png
cp -p resources/images/viewer.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/calibre-viewer.png

# these are provided as separate packages
rm -rf %{buildroot}%{_libdir}/%{name}/{odf,cherrypy,encutils,cssutils}
rm -rf %{buildroot}%{_libdir}/%{name}/cal/utils/genshi
rm -rf %{buildroot}%{_libdir}/%{name}/cal/trac

# rm empty feedparser files.
rm -rf %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.*

ln -s %{python_sitelib}/feedparser.py \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.py
ln -s %{python_sitelib}/feedparser.pyc \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.pyc
ln -s %{python_sitelib}/feedparser.pyo \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.pyo

# link to system fonts after we have deleted (see Source0) the non-free ones
# http://bugs.calibre-ebook.com/ticket/3832
ln -s %{_datadir}/fonts/LiberationMono-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-BoldItalic.ttf
ln -s %{_datadir}/fonts/LiberationMono-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Bold.ttf
ln -s %{_datadir}/fonts/LiberationMono-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Italic.ttf
ln -s %{_datadir}/fonts/LiberationMono-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Regular.ttf
ln -s %{_datadir}/fonts/LiberationSans-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-BoldItalic.ttf
ln -s %{_datadir}/fonts/LiberationSans-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/LiberationSans-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Italic.ttf
ln -s %{_datadir}/fonts/LiberationSans-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Regular.ttf
ln -s %{_datadir}/fonts/LiberationSerif-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-BoldItalic.ttf
ln -s %{_datadir}/fonts/LiberationSerif-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Bold.ttf
ln -s %{_datadir}/fonts/LiberationSerif-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Italic.ttf
ln -s %{_datadir}/fonts/LiberationSerif-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Regular.ttf

# delete locales, calibre stores them in a zip file now
rm -rf %{buildroot}%{_datadir}/%{name}/localization/locales/

rm -f %{buildroot}%{_bindir}/%{name}-uninstall

cp -p %{SOURCE2} %{buildroot}%{_bindir}/calibre-mount-helper

cp -p %{SOURCE3} %{buildroot}%{_datadir}/appdata/

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%preun
rm %{_datadir}/%{name}/viewer/mathjax

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database -n %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database -n %{_datadir}/mime &> /dev/null || :
ln -s %{_jsdir}/mathjax %{_datadir}/%{name}/viewer/

%files
%doc COPYRIGHT LICENSE Changelog.yaml
%{_bindir}/calibre
%{_bindir}/calibre-complete
%{_bindir}/calibre-customize
%{_bindir}/calibre-debug
%{_bindir}/calibre-parallel
%{_bindir}/calibre-server
%{_bindir}/calibre-smtp
%{_bindir}/calibre-mount-helper
%{_bindir}/calibredb
%{_bindir}/ebook-convert
%{_bindir}/ebook-device
%{_bindir}/ebook-meta
%{_bindir}/ebook-viewer
%{_bindir}/fetch-ebook-metadata
%{_bindir}/lrf2lrs
%{_bindir}/lrfviewer
%{_bindir}/lrs2lrf
%{_bindir}/markdown-calibre
%{_bindir}/web2disk
%{_bindir}/ebook-polish
%{_bindir}/ebook-edit
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/apps/calibre-gui.png
%{_datadir}/icons/hicolor/*/apps/calibre-ebook-edit.png
%{_datadir}/icons/hicolor/*/apps/calibre-viewer.png
%{python_sitelib}/init_calibre.py*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/appdata/calibre*.appdata.xml

%changelog
