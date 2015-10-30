Name:    calligra 
Version: 2.9.8
Release: 3%{?dist}
Summary: An integrated office suite

License: GPLv2+ and LGPLv2+
URL:     http://www.calligra-suite.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/calligra-%{version}/calligra-%{version}.tar.xz

# support disabling products we don't package yet
Patch2: calligra-2.9.0-disable_products.patch
Patch3: 0001-adapt-to-libwps-0.4.patch

BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: bzip2-devel bzip2
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: appstream-glib
BuildRequires: pkgconfig(eigen3)
BuildRequires: pkgconfig(exiv2) 
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: freeglut-devel
BuildRequires: gettext-devel
BuildRequires: giflib-devel
BuildRequires: pkgconfig(glew)
BuildRequires: pkgconfig(GraphicsMagick)
BuildRequires: pkgconfig(gsl) 
BuildRequires: kdelibs4-devel
BuildRequires: kdepimlibs-devel
BuildRequires: pkgconfig(QtGui) 
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(gl) pkgconfig(glu) 
BuildRequires: pkgconfig(libkactivities)
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(libvisio-0.1)
BuildRequires: pkgconfig(libetonyek-0.1)
BuildRequires: pkgconfig(libodfgen-0.1)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(libwpd-0.10)
BuildRequires: pkgconfig(libwpg-0.3)
BuildRequires: pkgconfig(libwps-0.4)
BuildRequires: libspnav-devel 
#BuildRequires: pkgconfig(OpenColorIO)
BuildRequires: pkgconfig(poppler-qt4)
BuildRequires: pkgconfig(libpng)
BuildRequires: libicu-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(OpenEXR)
BuildRequires: openjpeg-devel
BuildRequires: perl
BuildRequires: pkgconfig(poppler-qt4)
BuildRequires: pkgconfig(qca2)
BuildRequires: readline-devel
BuildRequires: pkgconfig(sqlite3)

%description
%{summary}.

%package -n krita
Summary:  A creative sketching and painting application 
# krita_raw_import filter
BuildRequires: libkdcraw-devel

%description -n krita
Krita is a creative sketching and painting application based on KOffice 
technology. Whether you want to create art paintings, cartoons, concept
art or textures, Krita supports most graphics tablets out of the box.
Krita’s vision statement is:
* Krita is a KDE program for sketching and painting, offering an end–to–end
  solution for creating digital painting files from scratch by masters.
* Fields of painting that Krita explicitly supports are concept art,
  creation of comics and textures for rendering.
* Modelled on existing real-world painting materials and workflows,
  Krita supports creative working by getting out of the way and with
  snappy response.

%prep
%setup -q
%patch2 -p1 -b .disable_products
%patch3 -p1 -b .libwps-0.4

## disable krita gemini/sketch too, not ready
sed -i \
  -e 's|add_subdirectory(sketch)|#add_subdirectory(sketch)|g' \
  -e 's|add_subdirectory(gemini)|#add_subdirectory(gemini)|g' \
  krita/CMakeLists.txt


%build
mkdir %{_target_platform}
pushd %{_target_platform}
#avoid use qt5 moc anyway.
%{cmake_kde4} \
    -Wno-dev \
    -DCMAKE_BUILD_TYPE=Release \
    -DPRODUCTSET=KRITA \
    -DWITH_Soprano=OFF \
    -DWITH_Okular=OFF \
    ..
popd

make %{?_smp_mflags} -C %{_target_platform}
%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
# shared-mime-info >= 0.6 includes image/openraster
rm -rf %{buildroot}%{_kde4_datadir}/mime/packages/krita_ora.xml
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_kde4_datadir}/kde4/apps/cmake

#we do not ship any devel package
rm -rf %{buildroot}%{_kde4_libdir}/libbasicflakes.so
rm -rf %{buildroot}%{_kde4_libdir}/libflake.so
rm -rf %{buildroot}%{_kde4_libdir}/libkoodf.so
rm -rf %{buildroot}%{_kde4_libdir}/libkoplugin.so
rm -rf %{buildroot}%{_kde4_libdir}/libkotext.so
rm -rf %{buildroot}%{_kde4_libdir}/libkotextlayout.so
rm -rf %{buildroot}%{_kde4_libdir}/libkovectorimage.so
rm -rf %{buildroot}%{_kde4_libdir}/libkoversion.so
rm -rf %{buildroot}%{_kde4_libdir}/libkowidgets.so
rm -rf %{buildroot}%{_kde4_libdir}/libkowidgetutils.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritacolor.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritaglobal.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritaimage.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritalibbrush.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritalibpaintop.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritapsd.so
rm -rf %{buildroot}%{_kde4_libdir}/libkritaui.so
rm -rf %{buildroot}%{_kde4_libdir}/libkundo2.so
rm -rf %{buildroot}%{_kde4_libdir}/libpigmentcms.so


%check
for appdata_file in %{buildroot}%{_kde4_datadir}/appdata/*.appdata.xml ; do
appstream-util validate-relax --nonet ${appdata_file} ||:
done
for desktop_file in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
desktop-file-validate ${desktop_file}  ||:
done


%post -n krita
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
touch --no-create %{_kde4_datadir}/mime ||:

%posttrans -n krita
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
update-mime-database -n %{_kde4_datadir}/mime &> /dev/null || :

%postun -n krita
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
touch --no-create %{_kde4_datadir}/mime ||:
update-mime-database -n %{_kde4_datadir}/mime &> /dev/null || :
fi

%files -n krita
%{_kde4_bindir}/krita
%{_kde4_bindir}/gmicparser

%{_kde4_libdir}/lib*.so.*
#unversioned so
%{_kde4_libdir}/libkritacolord.so

%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/kde4/plugins/imageformats/kimg_*.so

%{_kde4_datadir}/appdata/krita.appdata.xml
%{_kde4_datadir}/config/krita*.knsrc
%{_kde4_datadir}/config/kritarc
%{_kde4_datadir}/kde4/servicetypes/*.desktop

%{_kde4_datadir}/kde4/apps/kritaplugins
%{_kde4_datadir}/kde4/apps/calligra
%{_kde4_datadir}/kde4/apps/kritasketch
%{_kde4_datadir}/kde4/apps/color-schemes
%{_kde4_datadir}/kde4/apps/krita
%{_kde4_datadir}/kde4/apps/kritaanimation
%{_kde4_datadir}/kde4/apps/kritagemini

%{_kde4_datadir}/kde4/services/qimageioplugins/*.desktop
%{_kde4_datadir}/kde4/services/calligra/*.desktop
%dir %{_kde4_datadir}/kde4/services/ServiceMenus/calligra
%{_kde4_datadir}/kde4/services/ServiceMenus/calligra/krita_print.desktop
%{_kde4_datadir}/applications/kde4/krita.desktop
%{_kde4_datadir}/applications/kde4/krita_*.desktop
%{_kde4_datadir}/icons/hicolor/*/apps/calligrakrita.*
%{_kde4_datadir}/icons/oxygen/*/actions/*
%{_kde4_datadir}/mime/packages/wiki-format.xml
%{_kde4_datadir}/mime/packages/calligra_svm.xml
%{_kde4_datadir}/mime/packages/krita.xml
%dir %{_kde4_datadir}/color/icc/krita
%{_kde4_datadir}/color/icc/krita/*.icc
%{_kde4_datadir}/color/icc/krita/*.icm
%{_kde4_datadir}/color/icc/krita/README


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.9.8-3
- Rebuild

