%define c_ares_version 1.10.0

Name:	    wireshark	
Version:	1.12.7
Release:	1
Summary:	Network Analyzer

Group:		Extra/Runtime/Utility
License:	GPLv2+
URL:		http://www.wireshark.org
Source0:	http://www.wireshark.org/download/src/%{name}-%{version}.tar.bz2
Patch0:     wireshark-1.12.6-lua_5_3_0-1.patch

Source10:   http://c-ares.haxx.se/download/c-ares-%{c_ares_version}.tar.gz
Patch10:    0001-Use-RPM-compiler-options.patch

BuildRequires:  gtk3-devel, lua-devel	
BuildRequires:  libpcap-devel
BuildRequires:  libnl3-devel
BuildRequires:  sbc-devel

#for setcap
Requires(post):   libcap
Requires(post):   gtk3
Requires(post):   desktop-file-utils 
%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -a10
%patch0 -p1

pushd c-ares-%{c_ares_version}
%patch10 -p1
popd

%build
export CFLAGS="-fPIC"
export CXXFLAGS="-fPIC"
#use internal static libraries.
export PKG_CONFIG_PATH=`pwd`/internal_libs_root/lib/pkgconfig

export PATH=`pwd`/internal_libs_root/bin:$PATH

#build internal c-ares
pushd c-ares-%{c_ares_version}
./configure --prefix=`pwd`/../internal_libs_root --disable-shared --enable-static
make %{?_smp_mflags}
make install
popd

%configure \
        --with-ssl \
        --without-gnutls \
        --without-qt \
        --with-gtk3=yes \
        --with-c-ares=`pwd`/internal_libs_root \
        CFLAGS="-I`pwd`/internal_libs_root/include" \
        CPPFLAGS="-I`pwd`/internal_libs_root/include"

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

for i in 16 24 32 48 64 128 256
do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps
    install -m0644 image/wsicon"$i".png %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps/wireshark.png
done
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -m0644 image/wsicon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wireshark.svg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m0644 wireshark.desktop $RPM_BUILD_ROOT%{_datadir}/applications/wireshark.desktop

#rm -rf %{buildroot}%{_bindir}/wireshark-qt

rpmclean


%post
setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap 2>/dev/null ||:
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:


%files
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%dir %{_libdir}/wireshark
%{_libdir}/wireshark/*
%{_datadir}/applications/wireshark.desktop
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/wireshark
%{_datadir}/wireshark/*
%{_mandir}/man1/*
%{_mandir}/man4/*

