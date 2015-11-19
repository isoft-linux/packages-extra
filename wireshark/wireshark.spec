#lua 5.3 is rejected, waiting for patch.
Name: wireshark	
Version: 2.0.0 
Release: 2
Summary: Network Analyzer

License: GPLv2+
URL: http://www.wireshark.org
Source0: http://www.wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1: 90-wireshark-usbmon.rules

Patch0: wireshark-disable-vcsversion-display.patch
#BuildRequires: lua-devel

BuildRequires: libpcap-devel >= 0.9
BuildRequires: zlib-devel, bzip2-devel
BuildRequires: openssl-devel
BuildRequires: glib2-devel
BuildRequires: libelfutils-devel, krb5-devel
BuildRequires: pcre-devel
BuildRequires: gnutls-devel
BuildRequires: desktop-file-utils
BuildRequires: xdg-utils
BuildRequires: flex, bison
BuildRequires: libcap-devel
BuildRequires: libnl3-devel
BuildRequires: perl(Pod::Html)
BuildRequires: perl(Pod::Man)
BuildRequires: libgcrypt-devel
BuildRequires: GeoIP-devel
BuildRequires: c-ares-devel
BuildRequires: portaudio-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: sbc-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

#for setcap
Requires(post):   libcap
Requires(post):   gtk3
Requires(post):   desktop-file-utils 
%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q 
%patch0 -p1

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif

export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-fstack-protector-strong/-fstack-protector-all}
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export LDFLAGS="$LDFLAGS -pie"

autoreconf -ivf

%configure \
    --with-ssl \
    --with-gnutls \
    --with-qt=5 \
    --with-gtk3=no \
    --with-gtk2=no \
    --enable-ipv6 \
    --with-gnu-ld \
    --with-pic \
    --without-lua \
    --with-portaudio \
    --with-geoip \
    --with-ssl \
    --with-libnl

#remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Install python stuff.
mkdir -p %{buildroot}%{python_sitearch}
install -m 644 tools/wireshark_be.py tools/wireshark_gen.py  %{buildroot}%{python_sitearch}

mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/udev/rules.d/

rm -rf %{buildroot}%{_datadir}/applications/wireshark-gtk.desktop

for i in 16 24 32 48 64 128 256
do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps
    install -m0644 image/wsicon"$i".png %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps/wireshark.png
done
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -m0644 image/wsicon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wireshark.svg

%pre
getent group wireshark >/dev/null || groupadd -r wireshark
getent group usbmon >/dev/null || groupadd -r usbmon

%post
/sbin/ldconfig
/usr/bin/udevadm trigger --subsystem-match=usbmon
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%postun 
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/gnome &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

        touch --no-create %{_datadir}/mime/packages &> /dev/null || :
        update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap 2>/dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%{_sysconfdir}/udev/rules.d/90-wireshark-usbmon.rules
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%dir %{_libdir}/wireshark
%{_libdir}/wireshark/*
%{_datadir}/applications/wireshark.desktop
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/wireshark
%{_datadir}/wireshark/*
%{python_sitearch}/*
%{_datadir}/appdata/wireshark.appdata.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/wireshark.xml
%{_mandir}/man1/*
%{_mandir}/man4/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.12.7-2
- Rebuild

