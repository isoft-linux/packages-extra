#NOTE: system-cairo disable in mozconfig, it will cause a flash blink problem.
%define homepage about:blank
%define desktop_file_utils_version 0.9
%define firefox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%define version_internal    41.0 
%define firefoxdir 		%{_libdir}/firefox

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        %{version_internal} 
Release:        12
URL:            http://www.mozilla.org/projects/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        firefox-%{version_internal}.source.tar.xz

Source10:       firefox-mozconfig

Source20:       vendor.js
Source21:       firefox.desktop

Source100:      find-external-requires


Patch0:         firefox-install-dir.patch

Patch1:         rhbz-966424.patch
#hg clone http://www.rosenauer.org/hg/mozilla/ -r firefox41

Source200: kde.js
Patch10: firefox-branded-icons.patch
Patch11: firefox-kde.patch
Patch12: firefox-no-default-ualocale.patch
Patch13: mozilla-kde.patch
Patch14: mozilla-language.patch
Patch15: mozilla-nongnome-proxies.patch
Patch16: toolkit-download-folder.patch
Patch17: mozilla-icu-strncat.patch


BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
BuildRequires:  yasm
BuildRequires:  nss >= 3.17.1
Requires:       desktop-file-utils >= %{desktop_file_utils_version}
Requires:       hunspell
Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.


%prep
%setup -q -c
cd mozilla-release
%patch0 -p1

%patch1 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

rm  -rf .mozconfig
cp %{SOURCE10} .mozconfig

sed -i '/ac_cpp=/s/$CPPFLAGS/& -O2/' configure

%build
pushd mozilla-release

MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | \
                     %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
#export LDFLAGS="$LDFLAGS -Wl,-rpath,/usr/lib/firefox"

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

make -f client.mk build $MOZ_SMP_FLAGS
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd mozilla-release
#avoid make install failed.
DISTDIR=`find . -name obj-*-gnu`
install -D -m0644 %{SOURCE200} $DISTDIR/dist/bin/defaults/pref/kde.js

make -f client.mk install DESTDIR=$RPM_BUILD_ROOT INSTALL_SDK=

for i in 16 22 24 32 48 256; do
  install -Dm644 browser/branding/official/default$i.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/firefox.png
done
install -Dm644 browser/branding/official/content/icon64.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/firefox.png
install -Dm644 browser/branding/official/mozicon128.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/firefox.png
install -Dm644 browser/branding/official/content/about-logo.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/192x192/apps/firefox.png
install -Dm644 browser/branding/official/content/about-logo@2x.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/384x384/apps/firefox.png


install -Dm644 %{SOURCE20} $RPM_BUILD_ROOT%{_libdir}/firefox/browser/defaults/preferences/vendor.js
install -Dm644 %{SOURCE200} $RPM_BUILD_ROOT%{_libdir}/firefox/browser/defaults/preferences/kde.js

install -Dm644 %{SOURCE21} $RPM_BUILD_ROOT%{_datadir}/applications/firefox.desktop


  # Use system-provided dictionaries
rm -rf %{buildroot}%{_libdir}/firefox/{dictionaries,hyphenation}
ln -sf %{_datadir}/myspell %{buildroot}/usr/lib/firefox/dictionaries
ln -sf %{_datadir}/hyphen %{buildroot}/usr/lib/firefox/hyphenation

# set up the firefox start link 
#rm -rf $RPM_BUILD_ROOT%{_bindir}/firefox
#install -m0755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/firefox

popd #mozilla-release

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_datadir}/applications/*
%dir %{_libdir}/firefox
%{_libdir}/firefox/*
%{_bindir}/firefox
%{_datadir}/icons/hicolor/*/apps/firefox.png

%changelog
* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to 41.0

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update 40.0

* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- disable system-cairo in mozconfig, avoid flash plugin blink problem.

* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- add kde integration

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

