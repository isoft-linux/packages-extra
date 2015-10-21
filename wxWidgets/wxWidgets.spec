%define withgtk2 1

Name:           wxWidgets
Version:        3.0.2
Release:        3 
Summary:        wxWidgets GUI library
License:        wxWidgets Library Licence
Group:          System Environment/Libraries
URL:            http://www.wxwidgets.org/
Source0:        http://dl.sf.net/wxwindows/%{name}-%{version}.tar.bz2
Patch0:         wxwidgets-make-c++-abicheck-not-fatal.patch

BuildRequires:  gtk3-devel, zlib-devel >= 1.1.4
BuildRequires:  libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  expat-devel
BuildRequires:  libGL-devel, libGLU-devel

%if %{withgtk2}
BuildRequires:  gtk2-devel
%endif

%description
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        common 
Summary:        Common libraries and utilities for the wxWidgets.
Group:          System Environment/Libraries

%description    common 
wxWidgets is a C++ library that lets developers create applications for Windows, Mac OS X, Linux and other platforms with a single code base
This package include common libraries and utilities for the wxWidgets.

%package        common-static-devel
Group:          Development/Libraries
Summary:        Common static development files for the wxWidgets.
Requires:       %{name}-common-devel = %{version}-%{release}

%description common-static-devel
This package include static development files needed to link with the wxWidgets.

%package        common-shared-devel
Group:          Development/Libraries
Summary:        Common shared development files for the wxWidgets.
Requires:       %{name}-common-devel = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}

%description common-shared-devel
This package include shared development files needed to link with the wxWidgets.

%package        common-devel
Group:          Development/Libraries
Summary:        Common development files for the wxWidgets. 

%description common-devel
This package include files needed to develop program with the wxWidgets.


%package        gtk2 
Summary:        wxWidgets/GTK2 libraries and utilities for the wxWidgets.
Group:          System Environment/Libraries
Requires:       %{name}-common

%description    gtk2 
wxWidgets/GTK2 libraries and utilities for the wxWidgets.

%package        gtk2-static-devel
Group:          Development/Libraries
Summary:        wxWidgets/GTK2 static development files for the wxWidgets.
Requires:       %{name}-common-static-devel = %{version}-%{release}
Requires:       %{name}-common-devel = %{version}-%{release}

%description gtk2-static-devel
This package include static wxWidgets/GTK2 development files needed to link with the wxWidgets. 

%package        gtk2-shared-devel
Group:          Development/Libraries
Summary:        wxWidgets/GTK2 development files for the wxWidgets.
Requires:       gtk2-devel
Requires:       %{name}-gtk2 = %{version}-%{release}
Requires:       %{name}-common-devel = %{version}-%{release}
Requires:       %{name}-common-shared-devel = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}

%description gtk2-shared-devel
This package include wxWidgets/GTK2 files needed to compile with the wxWidgets.



%package        gtk3
Summary:        wxWidgets/GTK3 libraries and utilities for the wxWidgets.
Group:          System Environment/Libraries
Requires:       %{name}-common

%description    gtk3
wxWidgets/GTK3 libraries and utilities for the wxWidgets.

%package        gtk3-static-devel
Group:          Development/Libraries
Summary:        wxWidgets/GTK3 static development files for the wxWidgets.
Requires:       %{name}-common-static-devel = %{version}-%{release}
Requires:       %{name}-common-devel = %{version}-%{release}

%description gtk3-static-devel
This package include static wxWidgets/GTK2 development files needed to link with the wxWidgets.

%package        gtk3-shared-devel
Group:          Development/Libraries
Summary:        wxWidgets/GTK3 development files for the wxWidgets.
Requires:       gtk3-devel
Requires:       %{name}-gtk3 = %{version}-%{release}
Requires:       %{name}-common-devel = %{version}-%{release}
Requires:       %{name}-common-shared-devel = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}

%description gtk3-shared-devel
This package include wxWidgets/GTK3 files needed to compile with the wxWidgets.

# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).

# --disable-mediactrl to drop dependency on old gstreamer, until wxWidgets support gstreamer-1.0

%define common_args --enable-unicode --enable-compat26 --enable-compat28 --enable-richtext --enable-aui --enable-xrc --enable-html --enable-htmlhelp --enable-sound --disable-mediactrl --enable-protocols --enable-ftp --enable-http --enable-fileproto --enable-ipv6 --enable-ipc --enable-epollloop --enable-datetime --enable-cmdline --enable-base64 --enable-dynamicloader --enable-file --enable-filesystem --enable-fontenum --enable-fontmap --enable-fs_archive --enable-fs_inet --enable-fs_zip --enable-fsvolume --enable-fswatcher --enable-mimetype --enable-tarstream --enable-textbuf --enable-timer --enable-zipstream --enable-url --enable-ribbon --enable-stc --enable-mdi --enable-mdidoc --enable-svg --disable-webview --enable-clipboard --enable-dnd --enable-markup --enable-accel --enable-animatectrl --enable-bannerwindow --enable-calendar --enable-caret --with-opengl --without-sdl --without-gnomeprint --disable-optimise

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

sed -i -e 's|/usr/lib\b|%{_libdir}|' wx-config.in configure
sed -i -e 's/lib64/lib/g' configure

%build

mkdir shared-gtk2
pushd shared-gtk2
ln -s ../configure .
%configure \
  --with-gtk=2 \
  --enable-shared \
  --enable-soname \
  %{common_args}

make %{?_smp_mflags}
popd


mkdir static-gtk2
pushd static-gtk2
ln -s ../configure .
%configure \
  --with-gtk=2 \
  --disable-shared \
  %{common_args}

make %{?_smp_mflags}
popd


mkdir shared
pushd shared
ln -s ../configure .
# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).
%configure \
  --with-gtk=3 \
  --enable-shared \
  --enable-soname \
  %{common_args}

make %{?_smp_mflags}
popd

mkdir static
pushd static 
ln -s ../configure .
%configure \
  --with-gtk=3 \
  --disable-shared \
  %{common_args}

make %{?_smp_mflags}
popd

pushd locale
make allmo
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd shared-gtk2 
%makeinstall
popd

pushd static-gtk2 
%makeinstall
popd

pushd shared 
%makeinstall
popd

#static installation should be the last one, since some binary command should be static linked.
pushd static 
%makeinstall
popd

#we prefer the static link for app based on wxWidgets.
rm $RPM_BUILD_ROOT%{_bindir}/wx-config
cp $RPM_BUILD_ROOT/%{_libdir}/wx/config/gtk3-unicode-static-3.0 $RPM_BUILD_ROOT%{_bindir}/wx-config

%find_lang wxstd
%find_lang wxmsw
cat wxmsw.lang >>wxstd.lang

#process demos and samples

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/wxWidgets
cp -r demos samples docs $RPM_BUILD_ROOT/%{_docdir}/wxWidgets
pushd $RPM_BUILD_ROOT/%{_docdir}/wxWidgets/demos
    find . -name makefile.bcc|xargs rm -rf
    find . -name *.vcproj|xargs rm -rf
    find . -name makefile.gcc|xargs rm -rf
    find . -name Makefile.in|xargs rm -rf
    find . -name makefile.vc|xargs rm -rf
    find . -name makefile.wat|xargs rm -rf
    find . -name *.dsp|xargs rm -rf
    rm -rf *.bkl
    find . -name *.bkl|xargs rm -rf
    rm -rf *.mms
    find . -name *.mms|xargs rm -rf
    
    for i in `find . -type d`;
    do
        pushd $i
        if [ -f makefile.unx ]; then
            mv makefile.unx Makefile
        fi
        popd
    done
popd

pushd $RPM_BUILD_ROOT/%{_docdir}/wxWidgets/samples
    find . -name makefile.bcc|xargs rm -rf
    find . -name *.vcproj|xargs rm -rf
    find . -name makefile.gcc|xargs rm -rf
    find . -name Makefile.in|xargs rm -rf
    find . -name makefile.vc|xargs rm -rf
    find . -name makefile.wat|xargs rm -rf
    find . -name *.dsp|xargs rm -rf
    rm -rf *.bkl
    find . -name *.bkl|xargs rm -rf
    rm -rf *.mms
    find . -name *.mms|xargs rm -rf

    for i in `find . -type d`;
    do
        pushd $i
        if [ -f makefile.unx ]; then
            mv makefile.unx Makefile
        fi
        popd
    done
popd


rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gtk2 -p /sbin/ldconfig
%postun gtk2 -p /sbin/ldconfig

%post gtk3 -p /sbin/ldconfig
%postun gtk3 -p /sbin/ldconfig

%files common -f wxstd.lang 
%defattr(-,root,root,-)
%{_libdir}/libwx_baseu*-3.0.so.*

%files common-static-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_baseu*-3.0.a
%{_libdir}/libwxregexu-3.0.a
%{_libdir}/libwxscintilla-3.0.a

%files common-shared-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_baseu*-3.0.so

%files common-devel
%defattr(-,root,root,-)
%{_bindir}/wxrc
%{_bindir}/wxrc-3.0
%{_bindir}/wx-config
%dir %{_includedir}/wx-3.0
%{_includedir}/wx-3.0/*
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*
%dir %{_docdir}/wxWidgets
%{_docdir}/wxWidgets/*

%files gtk2
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_*.so.*

%files gtk2-static-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_*.a
%{_libdir}/wx/config/gtk2-unicode-static-3.0
%{_libdir}/wx/include/gtk2-unicode-static-3.0

%files gtk2-shared-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_*.so
%{_libdir}/wx/config/gtk2-unicode-3.0
%{_libdir}/wx/include/gtk2-unicode-3.0


%files gtk3
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk3u_*.so.*

%files gtk3-static-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk3u_*.a
%{_libdir}/wx/config/gtk3-unicode-static-3.0
%{_libdir}/wx/include/gtk3-unicode-static-3.0

%files gtk3-shared-devel
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk3u_*.so
%{_libdir}/wx/config/gtk3-unicode-3.0
%{_libdir}/wx/include/gtk3-unicode-3.0

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

