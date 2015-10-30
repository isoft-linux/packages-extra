%global mozappdir     %{_libdir}/%{name}

Summary:        XUL Runtime for Gecko Applications
Name:           xulrunner
Version:        41.0.2
Release:        4%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Source0:        http://ftp.mozilla.org/pub/mozilla.org/xulrunner/releases/%{version}/source/xulrunner-%{version}.source.tar.xz
Source10:       %{name}-mozconfig
Source12:       %{name}-default-prefs.js
Source21:       %{name}.sh.in

# build patches
Patch1:         xulrunner-install-dir.patch
Patch2:         firefox-build.patch
Patch3:         mozilla-build-arm.patch
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
Patch19:        xulrunner-24.0-s390-inlines.patch
Patch20:        firefox-build-prbool.patch
Patch21:        aarch64-fix-skia.patch
Patch22:        mozilla-1005535.patch
Patch24:        rhbz-1219542-s390-build.patch

Patch200:        mozilla-193-pkgconfig.patch
# Unable to install addons from https pages
Patch204:        rhbz-966424.patch

# Upstream patches

# ---------------------------------------------------

BuildRequires:  nspr-devel
BuildRequires:  nss-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libcurl-devel
BuildRequires:  libvpx-devel
BuildRequires:  autoconf213
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  sqlite-devel
BuildRequires:  libffi-devel

Requires:       nspr
Requires:       nss
Requires:       sqlite


%description
XULRunner is a Mozilla runtime package that can be used to bootstrap XUL+XPCOM
applications that are as rich as Firefox and Thunderbird. It provides mechanisms
for installing, upgrading, and uninstalling these applications. XULRunner also
provides libxul, a solution which allows the embedding of Mozilla technologies
in other projects and products.

%package devel
Summary: Development files for Gecko

Requires: xulrunner = %{version}-%{release}
Requires: nspr-devel
Requires: nss-devel
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel
Requires: libXt-devel
Requires: libXrender-devel
Requires: hunspell-devel
Requires: sqlite-devel
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
Requires: libvpx-devel

%description devel
This package contains the libraries amd header files that are needed
for writing XUL+XPCOM applications with Mozilla XULRunner and Gecko.

%prep
%setup -q -c
cd mozilla-release

%patch1  -p1
%patch2  -p2 -b .build
%patch3  -p2 -b .arm
%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .s390-inlines
%patch20 -p1 -b .prbool
%patch21 -p1 -b .aarch64-fix-skia
%patch22 -p1 -b .mozilla-1005535
%ifarch s390
%patch24 -p1 -b .rhbz-1219542-s390
%endif

%patch200 -p2 -b .pk
%patch204 -p2 -b .966424

# Upstream patches


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

#---------------------------------------------------------------------

%build
cd mozilla-release 

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
# 
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-Wall//')
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS -fpermissive"
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64 %{arm}
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

#---------------------------------------------------------------------

%install
cd mozilla-release

# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE12} objdir/dist/bin/defaults/pref/all-isoft.js

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{name}
install -m 0755 %{SOURCE21} $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{name}-config

# install install_app.py
%{__cp} objdir/dist/bin/install_app.py $RPM_BUILD_ROOT%{mozappdir}

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Link libraries in sdk directory instead of copying them:
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{version}/sdk/lib
for i in *.so; do
     rm $i
     ln -s %{mozappdir}/$i $i
done
popd

# Move sdk/bin to xulrunner libdir
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{version}/sdk/bin
mv ply *.py $RPM_BUILD_ROOT%{mozappdir}
popd
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{version}/sdk/bin

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Install xpcshell
%{__cp} objdir/dist/bin/xpcshell $RPM_BUILD_ROOT/%{mozappdir}

# Install run-mozilla.sh
%{__cp} objdir/dist/bin/run-mozilla.sh $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Remove tmp files
find $RPM_BUILD_ROOT/%{mozappdir} -name '.mkdir.done' -exec rm -rf {} \;

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

#---------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/xulrunner
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.xulrunner
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%{mozappdir}/omni.ja
%{mozappdir}/*.so
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%{mozappdir}/install_app.py
%ghost %{mozappdir}/install_app.pyc
%ghost %{mozappdir}/install_app.pyo
%{mozappdir}/gmp-fake*/*

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}-devel-*
%{_datadir}/idl/%{name}*%{version}
%{_includedir}/%{name}*%{version}
%{_libdir}/%{name}-devel-*/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/*.py
%ghost %{mozappdir}/*.pyc
%ghost %{mozappdir}/*.pyo
%dir %{mozappdir}/ply
%{mozappdir}/ply/*.py
%ghost %{mozappdir}/ply/*.pyc
%ghost %{mozappdir}/ply/*.pyo

#---------------------------------------------------------------------

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-4
- Rebuild

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 41.0.2-3
- Initial build

