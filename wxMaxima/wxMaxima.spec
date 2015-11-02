Summary: Graphical user interface for Maxima 
Name:    wxMaxima
Version: 15.08.2
Release: 1%{?dist}

License: GPLv2+
URL:     http://wxmaxima.sourceforge.net/
Source0: http://downloads.sourceforge.net/wxmaxima/wxmaxima-%{version}.tar.gz
# replace poor upstream one for now
Source1: wxmaxima.desktop

ExclusiveArch: %{arm} %{ix86} x86_64 aarch64 ppc sparcv9 %{power64}

BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: wxWidgets-gtk3-static-devel
BuildRequires: appstream-glib
BuildRequires: libxml2-devel
BuildRequires: ImageMagick

Provides: wxmaxima = %{version}-%{release}

Requires: jsmath-fonts
Requires: maxima >= 5.30

%description
A Graphical user interface for the computer algebra system
Maxima using wxWidgets.


%prep
%setup -q -n wxmaxima-%{version}


%build
%configure \
  --with-wx-config=/usr/bin/wx-config-3.0

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

desktop-file-install --vendor="" \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# app icon
install -p -D -m644 data/wxmaxima.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wxmaxima.svg
install -p -D -m644 data/wxmaxima.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/wxmaxima.png
convert -resize 48x48 data/wxmaxima.png data/wxmaxima-48x48.png
install -p -D -m644 data/wxmaxima-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/wxmaxima.png

# mime icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/
install -p -m644 data/text-x-wx*.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/

%find_lang wxMaxima 

# Unpackaged files
rm -fv %{buildroot}%{_datadir}/wxMaxima/{COPYING,README}
rm -fv %{buildroot}%{_datadir}/applications/wxMaxima.desktop
rm -rf %{buildroot}%{_datadir}/info
rm -rfv %{buildroot}%{_datadir}/pixmaps/
rm -rfv %{buildroot}%{_datadir}/menu


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/wxmaxima.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/wxmaxima.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f wxMaxima.lang
%doc AUTHORS ChangeLog README
%license COPYING
%{_bindir}/wxmaxima
%{_datadir}/wxMaxima/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/wxmaxima.desktop
%{_datadir}/appdata/wxmaxima.appdata.xml
%{_datadir}/bash-completion/completions/wxmaxima
%{_datadir}/mime/packages/x-wxmathml.xml
%{_datadir}/mime/packages/x-wxmaxima-batch.xml
%{_docdir}/wxmaxima/
%{_mandir}/man1/wxmaxima.1*


%changelog
