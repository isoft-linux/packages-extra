Name:	    audacious-plugins	
Version:	3.7
Release:	1
Summary:	Plugins for audacious audio player

License:    see license in source	
URL:		http://audacious-media-player.org
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}-alpha1.tar.bz2
Patch0:     audacious-skin-do-not-use-bitmap-font.patch

BuildRequires:  audacious-devel	
BuildRequires:  libmpg123-devel
BuildRequires:  neon-devel
BuildRequires:  libcue-devel

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
%setup -q -n %{name}-%{version}-alpha1
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
%{_libdir}/audacious/
%{_datadir}/audacious/
