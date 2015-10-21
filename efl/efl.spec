%global with_x11 1

Summary: Enlightenment Foundation Libraries
Name: efl
Version: 1.15.2
Release: 1
License: LGPLv2.1 GPLv2.1 BSD
URL: http://www.enlightenment.org/
Source: http://download.enlightenment.org/rel/libs/efl/efl-%{version}.tar.gz
Patch0: efl-ecore-wayland-should-depend-on-wayland.patch

BuildRequires: libjpeg-devel, zlib-devel, giflib-devel
BuildRequires: mesa-libGL-devel
BuildRequires: libX11-devel, libXinerama-devel, libXrender-devel, libXScrnSaver-devel, libXp-devel
BuildRequires: bullet-devel
BuildRequires: luajit-devel >= 2.0
BuildRequires: fribidi-devel
BuildRequires: libsndfile-devel

Requires(post): shared-mime-info
Requires(postun): shared-mime-info

%description
The Enlightenment Foundation Libraries are a collection of libraries
and tools upon which sophisticated graphical applications can be
built.  Included are a data structure library (Eina), a C-based object
engine (EO), a data storage library (EET), an object canvas (Evas),
and more.

%package devel
Summary: EFL headers, static libraries,and test programs
Requires: %{name} = %{version}

%description devel
Headers, static libraries, test programs for EFL.

%package doc
Summary: EFL API documents
Requires: %{name} = %{version}

%description doc
EFL API documents.

%prep
%setup -q 
%patch0 -p1


%build
export CC=clang
export CXX=clang++
%configure \
    --enable-systemd \
    --enable-wayland \
    --enable-egl \
    --enable-image-loader-webp \
    --enable-harfbuzz \
    %if %with_x11
    --with-opengl=full \
    --with-x11=xlib \
    --with-x \
    %else
    --with-opengl=es \
    --with-x11=none \
    --without-x \
    --enable-i-really-know-what-i-am-doing-and-that-this-will-probably-break-things-and-i-will-fix-them-myself-and-send-patches-aba
    %endif

make %{?_smp_mflags}
make doc

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/efl-api
cp -r doc/html/* $RPM_BUILD_ROOT/usr/share/doc/efl-api

%{find_lang} %{name}

%clean
test "x$RPM_BUILD_ROOT" != "x/" && rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
update-mime-database /usr/share/mime >/dev/null 2>&1 ||:

%postun
/sbin/ldconfig
update-mime-database /usr/share/mime >/dev/null 2>&1 ||:

%files -f %{name}.lang
%{_bindir}/ecore_evas_convert
%{_bindir}/eeze_disk_ls
%{_bindir}/eeze_mount
%{_bindir}/eeze_scanner
%{_bindir}/eeze_umount
%{_bindir}/efreetd
%{_bindir}/ethumb
%{_bindir}/ethumbd
%{_bindir}/ethumbd_client
%dir %{_libdir}/ecore
%dir %{_libdir}/ecore_evas
%dir %{_libdir}/ecore_imf
%dir %{_libdir}/edje
%dir %{_libdir}/eeze
%dir %{_libdir}/efreet
%dir %{_libdir}/emotion
%dir %{_libdir}/ethumb
%dir %{_libdir}/ethumb_client
%dir %{_libdir}/evas
%{_libdir}/ecore/*
%{_libdir}/ecore_evas/*
%{_libdir}/ecore_imf/*
%{_libdir}/edje/*
%{_libdir}/eeze/*
%{_libdir}/efreet/*
%{_libdir}/emotion/*
%{_libdir}/ethumb/*
%{_libdir}/ethumb_client/*
%{_libdir}/evas/*


%{_libdir}/lib*.so.*
#%{_libdir}/systemd/user/efreet.service
%{_libdir}/systemd/user/ethumb.service
#%{_datadir}/dbus-1/services/org.enlightenment.Efreet.service
%{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service
%dir %{_datadir}/ecore
%dir %{_datadir}/ecore_imf
%dir %{_datadir}/edje
%dir %{_datadir}/eeze
%dir %{_datadir}/efreet
%dir %{_datadir}/elua
%dir %{_datadir}/embryo
%dir %{_datadir}/emotion
%dir %{_datadir}/eo
%dir %{_datadir}/eolian
%dir %{_datadir}/ethumb
%dir %{_datadir}/ethumb_client
%dir %{_datadir}/evas

%{_datadir}/ecore/*
%{_datadir}/ecore_imf/*
%{_datadir}/eeze/*
%{_datadir}/efreet/*
%{_datadir}/elua/*
%{_datadir}/emotion/*
%{_datadir}/ethumb/*
%{_datadir}/ethumb_client/*
%{_datadir}/evas/*
%{_datadir}/mime/packages/edje.xml

%if %with_x11
%dir %{_datadir}/ecore_x
%{_datadir}/ecore_x/*
%dir %{_libdir}/ecore_x
%{_libdir}/ecore_x/*
%endif

%files devel
%{_bindir}/edje_cc
%{_bindir}/edje_codegen
%{_bindir}/edje_decc
%{_bindir}/edje_external_inspector
%{_bindir}/edje_inspector
%{_bindir}/edje_pick
%{_bindir}/edje_player
%{_bindir}/edje_recc
%{_bindir}/edje_watch
%{_bindir}/eet
%{_bindir}/eina-bench-cmp
%{_bindir}/eldbus-codegen
%{_bindir}/elua
%{_bindir}/embryo_cc
%{_bindir}/eolian_cxx
%{_bindir}/eolian_gen
%{_bindir}/evas_cserve2_client
%{_bindir}/evas_cserve2_debug
%{_bindir}/evas_cserve2_shm_debug
%{_bindir}/evas_cserve2_usage
%{_bindir}/vieet
%{_bindir}/diffeet
%{_bindir}/eetpack
%{_bindir}/efl_debug
%{_bindir}/efl_debugd
%{_bindir}/eina_btlog

%{_includedir}/*
%{_libdir}/*.so

%dir %{_datadir}/edje/include
%dir %{_datadir}/embryo/include
%dir %{_datadir}/eo/gdb
%dir %{_datadir}/eolian/include
%{_datadir}/edje/include/*
%{_datadir}/embryo/include/*
%{_datadir}/eo/gdb/*
%{_datadir}/eolian/include/*

%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*
%{_datadir}/gdb/auto-load/usr/lib/libeo.so.*-gdb.py

%files doc
%dir %{_datadir}/doc/efl-api
%{_datadir}/doc/efl-api/*

%changelog
* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 1.15.2
* Tue Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update to 1.15.0

