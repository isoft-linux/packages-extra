%define libexif_version 0.6.16
%define exiv2_ver 0.24
%define babl_ver 0.1.10
%define gegl_ver 0.2.0

# mp:          multi processor support
%bcond_without mp
# print:       build the print plugin (if you don't build it externally)
%bcond_without print
# gutenprint:  require gutenprint-plugin (instead of gimp-print-plugin) if
#              internal print plugin isn't built
%bcond_without gutenprint
# convenience: install convenience symlinks
%bcond_without convenience

Summary:        GNU Image Manipulation Program
Name:           gimp
Epoch:          2
Version:        2.8.14
Release:        2 
%define binver 2.8
%define gimp_lang_ver 20
%define interfacever 2.0
%define age 0
%define minorver 704 
#%define microver %(ver=%{version}; echo ${ver##*.*.})
%define microver 0 
License:        GPLv2+
URL:            http://www.gimp.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%__id_u -n)
Obsoletes:      gimp-perl < 2:2.0
Obsoletes:      gimp < 2:2.6.0-3
BuildRequires:  alsa-lib-devel >= 1.0.0
BuildRequires:  cairo-devel >= 1.4.10
BuildRequires:  libcurl-devel >= 7.15.1
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  fontconfig-devel >= 2.2.0
BuildRequires:  freetype-devel >= 2.1.7
BuildRequires:  glib2-devel >= 2.16.1
BuildRequires:  gtk2-devel >= 2.12.5
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel >= 2.14.0
BuildRequires:  libtiff-devel
BuildRequires:  pango-devel >= 1.18.0
BuildRequires:  poppler-glib-devel >= 0.4.1
BuildRequires:  libX11-devel
BuildRequires:  libXmu-devel
BuildRequires:  sed
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  findutils

Requires:       gimp-libs-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       glib2 >= 2.16.1
Requires:       gtk2 >= 2.12.5
Requires:       pango >= 1.18.0
Requires:       freetype >= 2.1.7
Requires:       fontconfig >= 2.2.0
%if ! %{with print}
%if %{with gutenprint}
Requires:       gutenprint-plugin
%else
Requires:       gimp-print-plugin
%endif
%endif
Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       gimp-libs-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       gimp-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}

Source0:        ftp://ftp.gimp.org/pub/gimp/v%{binver}/gimp-%{version}.tar.bz2
Source1:        gimp-plugin-mgr.in
# distro specific: use xdg-open instead of firefox as web browser
Patch0:         gimp-2.6.2-xdg-open.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=559081
# "JPEG Save dialog preview should adjust size units"
Patch1:         gimp-2.6.2-jpeg-units.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=556896
# "Dialogs don't get minimized with single image window"
Patch2:         gimp-2.6.6-minimize-dialogs.patch

Patch3:         gimp-pdf-do-not-belong-to-you.patch


%description
GIMP (GNU Image Manipulation Program) is a powerful image composition and
editing program, which can be extremely useful for creating logos and other
graphics for webpages. GIMP has many of the tools and filters you would expect
to find in similar commercial offerings, and some interesting extras as well.
GIMP provides a large image manipulation toolbox, including channel operations
and layers, effects, sub-pixel imaging and anti-aliasing, and conversions, all
with multi-level undo.

%package libs
Summary:        GIMP libraries
License:        LGPLv2+
Provides:       gimp-libs-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
The gimp-libs package contains shared libraries needed for the GNU Image
Manipulation Program (GIMP).

%package devel
Summary:        GIMP plugin and extension development kit
License:        LGPLv2+
Requires:       gimp-libs-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gimp-devel-tools = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gtk2-devel
Requires:       glib2-devel
Requires:       pkgconfig

%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.

%package devel-tools
Summary:        GIMP plugin and extension development tools
License:        LGPLv2+
Requires:       gimp-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel-tools
The gimp-devel-tools package contains gimptool, a helper program to build GNU
Image Manipulation Program (GIMP) plug-ins and extensions.

#%package help-browser
#Summary:        GIMP help browser plug-in
#Group:          Applications/Multimedia
#License:        GPLv2+
#Obsoletes:      gimp < 2:2.6.0-3
#Requires:       gimp-%{_arch} = %{?epoch:%{epoch}:}%{version}-%{release}
#
#%description help-browser
#The gimp-help-browser package contains a lightweight help browser plugin for
#viewing GIMP online help.

%prep
%setup -q -n gimp-%{version} 


%build
export CC=clang
export CXX=clang++
%configure \
    --disable-python \
%if %{with mp}
    --enable-mp \
%else
    --disable-mp \
%endif
    --disable-static \
%if %{with print}
    --with-print \
%else
    --without-print \
%endif
    --with-lcms \
    --enable-gimp-console \
    --without-aa \
%ifos linux
    --with-linux-input \
%endif
    --with-libtiff \
    --with-libjpeg \
    --with-libpng \
    --without-libmng \
    --with-libexif \
    --with-librsvg \
    --with-poppler \
    --without-gnomevfs \
    --with-alsa \
    --with-dbus \
    --with-script-fu \
    --without-webkit

for i in `find plug-ins -name Makefile`;do sed -i -e 's/LDFLAGS =/LDFLAGS = -lm/g' $i;done
make %{?_smp_mflags}

# convenience stuff for external plugins (e.g. xsane)
sed -e 's|@GIMPPLUGINDIR@|%{_libdir}/gimp/%{interfacever}|g' < %{SOURCE1} > gimp-plugin-mgr

%install
rm -rf %{buildroot}

# makeinstall macro won't work here - libexec is overriden
make DESTDIR=%{buildroot} install

# remove rpaths
find %buildroot -type f -print0 | xargs -0 -L 20 chrpath --delete --keepgoing 2>/dev/null || :

%ifos linux
# remove .la files
find %buildroot -name \*.la -exec %__rm -f {} \;
%endif

#
# Plugins and modules change often (grab the executeable ones)
#
echo "%defattr (-, root, root)" > gimp-plugin-files
find %{buildroot}%{_libdir}/gimp/%{interfacever} -type f | sed "s@^%{buildroot}@@g" | grep -v '\.a$' >> gimp-plugin-files

#for file in $(cat gimp-plugin-files-py); do
#    for newfile in ${file}c ${file}o; do
#        fgrep -q -x "$newfile" gimp-plugin-files || echo "$newfile"
#    done
#done >> gimp-plugin-files


#
# Auto detect the lang files.
#
%find_lang gimp%{gimp_lang_ver}
%find_lang gimp%{gimp_lang_ver}-std-plug-ins
%find_lang gimp%{gimp_lang_ver}-script-fu
%find_lang gimp%{gimp_lang_ver}-libgimp
%find_lang gimp%{gimp_lang_ver}-tips
%find_lang gimp%{gimp_lang_ver}-python

cat gimp%{gimp_lang_ver}.lang gimp%{gimp_lang_ver}-std-plug-ins.lang gimp%{gimp_lang_ver}-script-fu.lang gimp%{gimp_lang_ver}-libgimp.lang gimp%{gimp_lang_ver}-tips.lang  gimp%{gimp_lang_ver}-python.lang > gimp-all.lang

#
# Build the master filelists generated from the above mess.
#
cat gimp-plugin-files gimp-all.lang > gimp.files

%if %{with convenience}
# install convenience symlinks
ln -snf gimp-%{binver} %{buildroot}%{_bindir}/gimp
ln -snf gimp-%{binver}.1 %{buildroot}%{_mandir}/man1/gimp.1
ln -snf gimp-console-%{binver} %{buildroot}/%{_bindir}/gimp-console
ln -snf gimp-console-%{binver}.1 %{buildroot}/%{_mandir}/man1/gimp-console.1
#ln -snf gimp-remote-%{binver} %{buildroot}%{_bindir}/gimp-remote
#ln -snf gimp-remote-%{binver}.1 %{buildroot}%{_mandir}/man1/gimp-remote.1
ln -snf gimptool-%{interfacever} %{buildroot}%{_bindir}/gimptool
ln -snf gimptool-%{interfacever}.1 %{buildroot}%{_mandir}/man1/gimptool.1
ln -snf gimprc-%{binver}.5 %{buildroot}/%{_mandir}/man5/gimprc.5
%endif

# convenience stuff for external plugins (e.g. xsane)
mkdir -p %{buildroot}%{_sysconfdir}/gimp/plugins.d
mkdir -p %{buildroot}%{_sbindir}
install -m 0755 gimp-plugin-mgr %{buildroot}%{_sbindir}/gimp-plugin-mgr


%clean
rm -rf %{buildroot}

%pre
# First, remove old symlinks which are possibly in an old location (before a
# major version update)
if [ -x "%{_sbindir}/gimp-plugin-mgr" ]; then
    %{_sbindir}/gimp-plugin-mgr --uninstall '*' || :
fi

%post
/usr/bin/update-desktop-database %{_datadir}/applications &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
# Then re-add the symlinks
%{_sbindir}/gimp-plugin-mgr --install '*' || :

%preun
# Only delete symlinks when uninstalling
if [ "$1" = "0" ]; then
    %{_sbindir}/gimp-plugin-mgr --uninstall '*' || :
fi

%postun
if [ "$1" = "0" ]; then
    /usr/bin/update-desktop-database %{_datadir}/applications &> /dev/null || :
fi
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f gimp.files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc docs/*.xcf*
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/gimp.appdata.xml
%dir %{_datadir}/gimp
%dir %{_datadir}/gimp/%{interfacever}
%{_datadir}/gimp/%{interfacever}/tips/
%{_datadir}/gimp/%{interfacever}/menus/
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{interfacever}
%dir %{_libdir}/gimp/%{interfacever}/environ
#%dir %{_libdir}/gimp/%{interfacever}/fonts
%dir %{_libdir}/gimp/%{interfacever}/interpreters
%dir %{_libdir}/gimp/%{interfacever}/modules
%{_libdir}/gimp/%{interfacever}/plug-ins
###%exclude %{_libdir}/gimp/%{interfacever}/plug-ins/help-browser
#%dir %{_libdir}/gimp/%{interfacever}/tool-plug-ins
%{_datadir}/gimp/*/ui/plug-ins/*
%{_datadir}/gimp/*/dynamics/*
%{_datadir}/gimp/*/tags/*

%{_datadir}/gimp/%{interfacever}/brushes/
%{_datadir}/gimp/%{interfacever}/fractalexplorer/
%{_datadir}/gimp/%{interfacever}/gfig/
%{_datadir}/gimp/%{interfacever}/gflare/
%{_datadir}/gimp/%{interfacever}/gimpressionist/
%{_datadir}/gimp/%{interfacever}/gradients/
# %{_datadir}/gimp/%{interfacever}/help/
%{_datadir}/gimp/%{interfacever}/images/
%{_datadir}/gimp/%{interfacever}/palettes/
%{_datadir}/gimp/%{interfacever}/patterns/
%{_datadir}/gimp/%{interfacever}/scripts/
%{_datadir}/gimp/%{interfacever}/themes/

%dir %{_sysconfdir}/gimp
%dir %{_sysconfdir}/gimp/plugins.d
%dir %{_sysconfdir}/gimp/%{interfacever}
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/controllerrc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/gimprc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/gtkrc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/unitrc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/sessionrc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/templaterc
%config(noreplace) %{_sysconfdir}/gimp/%{interfacever}/menurc

%{_bindir}/gimp-%{binver}
#%{_bindir}/gimp-remote-%{binver}
%{_bindir}/gimp-console-%{binver}
%{_sbindir}/gimp-plugin-mgr

%if %{with convenience}
%{_bindir}/gimp
#%{_bindir}/gimp-remote
%{_bindir}/gimp-console
%endif

%{_mandir}/man1/gimp-%{binver}.1*
#%{_mandir}/man1/gimp-remote-%{binver}.1*
%{_mandir}/man1/gimp-console-%{binver}.1*
%{_mandir}/man5/gimprc-%{binver}.5*

%if %{with convenience}
%{_mandir}/man1/gimp.1*
#%{_mandir}/man1/gimp-remote.1*
%{_mandir}/man1/gimp-console.1*
%{_mandir}/man5/gimprc.5*
%endif

%{_datadir}/icons/hicolor/*/apps/gimp.png





%{_libdir}/gimp/%{interfacever}/environ/default.env
%{_libdir}/gimp/%{interfacever}/interpreters/default.interp
%{_libdir}/gimp/%{interfacever}/modules/libcolor-selector-cmyk.so
%{_libdir}/gimp/%{interfacever}/modules/libcolor-selector-water.so
%{_libdir}/gimp/%{interfacever}/modules/libcolor-selector-wheel.so
%{_libdir}/gimp/%{interfacever}/modules/libcontroller-linux-input.so
%{_libdir}/gimp/%{interfacever}/modules/libcontroller-midi.so
%{_libdir}/gimp/%{interfacever}/modules/libdisplay-filter-color-blind.so
%{_libdir}/gimp/%{interfacever}/modules/libdisplay-filter-gamma.so
%{_libdir}/gimp/%{interfacever}/modules/libdisplay-filter-high-contrast.so


%{_datadir}/gimp/%{interfacever}/tool-presets/*

%files libs
%defattr(-, root, root, 0755)
%{_libdir}/libgimp*.so.*

%files devel
%defattr (-, root, root, 0755)
%doc HACKING README.i18n
%doc %{_datadir}/gtk-doc/*

%{_libdir}/*.so
%dir %{_libdir}/gimp
%dir %{_libdir}/gimp/%{interfacever}
%dir %{_libdir}/gimp/%{interfacever}/modules
%ifnos linux
%{_libdir}/*.la
%{_libdir}/gimp/%{interfacever}/modules/*.la
%endif
%{_datadir}/aclocal/*.m4
%{_includedir}/gimp-%{interfacever}
%{_libdir}/pkgconfig/*

%files devel-tools
%defattr (-, root, root, 0755)
%{_bindir}/gimptool-%{interfacever}
%{_mandir}/man1/gimptool-%{interfacever}.1*

%if %{with convenience}
%{_bindir}/gimptool
%{_mandir}/man1/gimptool.1*
%endif

#%files help-browser
#%defattr (-, root, root, 0755)
#%{_libdir}/gimp/%{interfacever}/plug-ins/help-browser

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2:2.8.14-2
- Rebuild

