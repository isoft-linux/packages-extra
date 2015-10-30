Name: audacious-plugins 
Version: 3.7
Release: 3
Summary: Plugins for audacious audio player

License: see license in source 
URL: http://audacious-media-player.org
Source0: http://distfiles.audacious-media-player.org/%{name}-%{version}-beta1.tar.bz2
Patch0: audacious-skin-do-not-use-bitmap-font.patch

BuildRequires: audacious-devel 
BuildRequires: libmpg123-devel
BuildRequires: neon-devel
BuildRequires: libcue-devel
BuildRequires: alsa-lib-devel
BuildRequires: faad2-devel
BuildRequires: ffmpeg-devel
BuildRequires: glib2-devel
BuildRequires: libflac-devel
BuildRequires: libogg-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: libxml2-devel
BuildRequires: mesa-libGL-devel
BuildRequires: neon-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtmultimedia
BuildRequires: wavpack-devel

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}-beta1
%patch0 -p1

%build
%configure \
 --disable-console \
 --disable-xsf \
 --disable-coreaudio \
 --disable-psf \
 --disable-filewriter_mp3 \
 --disable-gnomeshortcuts \
 --disable-lirc \
 --disable-ladspa \
 --disable-vtx \
 --disable-hotkey \
 --disable-gtk \
 --disable-aosd \
 --disable-aosd-xcomp \
 --disable-notify \
 --disable-sdlout \
 --enable-pulse \
 --enable-alsa \
 --enable-qt \
 --enable-mp3 \
 --enable-cue \
 --enable-aac \
 --enable-vorbis 

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%find_lang audacious-plugins 

%files -f audacious-plugins.lang 
%{_libdir}/audacious/*
%{_datadir}/audacious/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.7-3
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 3.7-2
- update

