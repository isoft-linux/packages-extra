#NOTE: system-cairo disable in mozconfig, it will cause a flash blink problem.

#we do not provide debuginfo of firefox.
%define debug_package %{nil}

#do not use kde integration
%global with_kde 0 

%define desktop_file_utils_version 0.9

%define version_internal 42.0
%define firefoxdir %{_libdir}/firefox

Summary: Mozilla Firefox Web browser
Name: firefox
Version: %{version_internal} 
Release: 2
URL: http://www.mozilla.org/projects/firefox/
License: MPLv1.1 or GPLv2+ or LGPLv2+
Source0: firefox-%{version_internal}.source.tar.xz

Source10: firefox-mozconfig

Source20: vendor.js
Source21: firefox.desktop

Source100: find-external-requires

Source200: kde.js

Patch0: firefox-install-dir.patch

Patch1: rhbz-966424.patch
#hg clone http://www.rosenauer.org/hg/mozilla/ -r firefox41

Patch10: firefox-branded-icons.patch
Patch11: firefox-kde.patch
Patch12: firefox-no-default-ualocale.patch
Patch13: mozilla-kde.patch
Patch14: mozilla-language.patch
Patch15: mozilla-nongnome-proxies.patch
Patch16: toolkit-download-folder.patch


BuildRequires: desktop-file-utils
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: zip
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: libIDL-devel

BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: krb5-devel
BuildRequires: pango-devel
BuildRequires: freetype-devel
BuildRequires: libXt-devel
BuildRequires: libXrender-devel
BuildRequires: libXinerama-devel
BuildRequires: libXcomposite-devel libXfixes-devel
BuildRequires: hunspell-devel
BuildRequires: startup-notification-devel
BuildRequires: alsa-lib-devel
BuildRequires: libnotify-devel
BuildRequires: mesa-libGL-devel
BuildRequires: libcurl-devel
BuildRequires: libvpx-devel
BuildRequires: autoconf213
BuildRequires: pulseaudio-libs-devel
BuildRequires: sqlite-devel
BuildRequires: libffi-devel
BuildRequires: libicu-devel
BuildRequires: yasm
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: GConf2-devel

Requires:       desktop-file-utils >= %{desktop_file_utils_version}
Requires:       hunspell
Provides:       webclient

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.


%prep
%setup -q -c
cd firefox-%{version} 
%patch0 -p1

%patch1 -p1
%patch10 -p1

%if %{with_kde}
%patch11 -p1
%endif

%patch12 -p1

%if %{with_kde}
%patch13 -p1
%endif

%patch14 -p1
%patch15 -p1
%patch16 -p1

rm  -rf .mozconfig
cp %{SOURCE10} .mozconfig

sed -i '/ac_cpp=/s/$CPPFLAGS/& -O2/' configure

%build
pushd firefox-%{version} 

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
pushd firefox-%{version} 
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

%if %{with_kde}
install -Dm644 %{SOURCE200} $RPM_BUILD_ROOT%{_libdir}/firefox/browser/defaults/preferences/kde.js
%endif

install -Dm644 %{SOURCE21} $RPM_BUILD_ROOT%{_datadir}/applications/firefox.desktop


# Use system-provided dictionaries
rm -rf %{buildroot}%{_libdir}/firefox/{dictionaries,hyphenation}
ln -sf %{_datadir}/myspell %{buildroot}/usr/lib/firefox/dictionaries
ln -sf %{_datadir}/hyphen %{buildroot}/usr/lib/firefox/hyphenation

# set up the firefox start link 
#rm -rf $RPM_BUILD_ROOT%{_bindir}/firefox
#install -m0755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/firefox

popd #mozilla-release

%clean
rm -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------
%post
touch --no-create %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :

%posttrans
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    fi
fi
update-desktop-database ||:

%files
%defattr(-,root,root,-)
%{_datadir}/applications/*
%dir %{_libdir}/firefox
%{_libdir}/firefox/*
%{_bindir}/firefox
%{_datadir}/icons/hicolor/*/apps/firefox.png

%changelog
* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 42.0-2
- Update to 42.0

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-15
- Rebuild with icu 56.1

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-14
- Rebuild

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-13
- Update to 41.0.2

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

