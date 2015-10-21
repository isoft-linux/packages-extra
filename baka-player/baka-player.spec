Name:		baka-player
Version:	2.0.3
Release:	1
Summary:	A free and open source, cross-platform, libmpv based multimedia player

License:    GPL	
URL:		http://bakamplayer.u8sand.net/
#git clone https://github.com/u8sand/Baka-MPlayer.git
Source0:    Baka-MPlayer.tar.gz	
Patch0:     Baka-MPlayer-add-mime-support.patch

BuildRequires:  libmpv-devel
BuildRequires:  qt5-qtdeclarative-devel qt5-qtsvg-devel	qt5-qttools
Requires:	mpv

%description
%{summary}

%prep
%setup -q -n Baka-MPlayer
%patch0 -p1

%build
mkdir -p build
pushd build
%{qmake_qt5} \
    ../src \
    CONFIG+=release \
    CONFIG+=install_translations

make %{?_smp_mflags}
popd

%install
pushd build
make install INSTALL_ROOT=%{buildroot}
popd

rm -rf $RPM_BUILD_ROOT%{_datadir}/licenses

%post
/usr/bin/update-desktop-database -q
xdg-icon-resource forceupdate --theme hicolor &> /dev/null

%postun
/usr/bin/update-desktop-database -q
xdg-icon-resource forceupdate --theme hicolor &> /dev/null


%files
%{_bindir}/baka-mplayer
%{_datadir}/applications/baka-mplayer.desktop
%{_datadir}/baka-mplayer
%{_docdir}/baka-mplayer/baka-mplayer.md
%{_datadir}/icons/hicolor/scalable/apps/baka-mplayer.svg
%{_mandir}/man1/baka-mplayer.1.gz
%{_datadir}/pixmaps/baka-mplayer.svg

%changelog
* Mon Jul 20 2015 Cjacker <cjacker@foxmail.com>
- add mime support to desktop file.
* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- first build
