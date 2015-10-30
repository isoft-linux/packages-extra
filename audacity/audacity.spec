Name: audacity
Version: 2.1.1
Release: 3%{?dist}
Summary: Multitrack audio editor
License: GPLv2
URL:     http://audacity.sourceforge.net

Source0: http://www.fosshub.com/Audacity.html/%{name}-minsrc-%{version}.tar.xz
Source1: http://www.fosshub.com/Audacity.html/%{name}-manual-%{version}.zip
#fix build with system ffmpeg header
Patch0: audacity-ffmpeg.patch
Patch1: audacity-fix-wx3-build.patch
Patch2: audacity-do-not-warn-me.patch

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel
BuildRequires: flac-devel
BuildRequires: gettext
BuildRequires: ffmpeg-devel
BuildRequires: libid3tag-devel
BuildRequires: taglib-devel
BuildRequires: libogg-devel
BuildRequires: libsndfile-devel
BuildRequires: libvorbis-devel
BuildRequires: zip
BuildRequires: zlib-devel
BuildRequires: wxGTK28-static-devel
BuildRequires: appstream-glib
BuildRequires: libmad-devel twolame-devel

%description
Audacity is a cross-platform multitrack audio editor. It allows you to
record sounds directly or to import files in various formats. It features
a few simple effects, all of the editing features you should need, and
unlimited undo. The GUI was built with wxWidgets and the audio I/O
supports PulseAudio, OSS and ALSA under Linux.

%prep
%setup -q -n %{name}-minsrc-%{version} 
%patch0 -p1
#used for wxGTK3
#%patch1 -p1
#%patch2 -p1

%build
%configure \
    --with-help \
    --with-libsndfile=system \
    --with-libsamplerate=system \
    --with-libflac=system \
    --with-vorbis=system \
    --with-id3tag=system \
    --with-expat=system \
    --with-libmad=system \
    --with-ffmpeg=system \
    --with-libsoxr \
    --with-libvamp \
    --with-portaudio \
    --with-libtwolame=system \
    --without-libresample \
    --without-ladspa \
    --without-soundtouch \
    --with-wx-config=`pwd`/gtk2-unicode-static-3.0 \
%ifnarch %{ix86} x86_64
    --disable-sse \
%else
    %{nil}
%endif

# _smp_mflags cause problems?
make %{?_smp_mflags}

rm -rf lib-src/ffmpeg

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm -Rf $RPM_BUILD_ROOT%{_datadir}/%{name}/include

# Audacity 1.3.8-beta complains if the help/manual directories
# don't exist.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/help/manual

%{find_lang} %{name}

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
        $RPM_BUILD_ROOT%{_datadir}/applications/audacity.desktop

# audacity manual must be unzipped to correct location
unzip %{SOURCE1} -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database -n %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database -n %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/EQDefaultCurves.xml
%{_datadir}/%{name}/nyquist/
%{_datadir}/%{name}/plug-ins/
%{_mandir}/man*/*
%{_datadir}/applications/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/mime/packages/*
%doc %{_datadir}/doc/*
%{_datadir}/%{name}/help/


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.1.1-3
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 2.1.1-2
- Initial build

