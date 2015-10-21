Name:           SDL_sound
Version:        1.0.3
Release:        15%{?dist}
Summary:        Library handling decoding of several popular sound file formats
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.icculus.org/SDL_sound
# This is:
# http://www.icculus.org/SDL_sound/downloads/%{name}-%{version}.tar.gz
# With all the files except the Makefiles under decoders/mpglib (patented)
# and PBProjects.tar.gz (contains binaries) removed
Source0:        %{name}-%{version}.tar.gz  
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  SDL-devel libflac-devel libspeex-devel libvorbis-devel libogg-devel
BuildRequires:  doxygen

%description
SDL_sound is a library that handles the decoding of several popular sound file 
formats, such as .WAV and .OGG.

It is meant to make the programmer's sound playback tasks simpler. The 
programmer gives SDL_sound a filename, or feeds it data directly from one of 
many sources, and then reads the decoded waveform data back at her leisure. 
If resource constraints are a concern, SDL_sound can process sound data in 
programmer-specified blocks. Alternately, SDL_sound can decode a whole sound 
file and hand back a single pointer to the whole waveform. SDL_sound can 
also handle sample rate, audio format, and channel conversion on-the-fly 
and behind-the-scenes, if the programmer desires.


%package        devel
Summary:        %{summary}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       SDL-devel

%description    devel
%{description}

This package contains the headers and libraries for SDL_sound development.


%prep
%setup -q
# Avoid lib64 rpaths
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure


%build
# no smpeg and internal mpglib because of patents!
%configure --disable-dependency-tracking --disable-static \
    --disable-smpeg --disable-mpglib --enable-mikmod --enable-ogg \
    --enable-modplug --enable-speex --enable-flac --enable-midi
make %{?_smp_mflags}
doxygen Doxyfile


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Add namespaces to man pages (livna bug #1181)
cp -a docs/man/man3 man3
pushd man3
mv actual.3 Sound_Sample::actual.3
mv author.3 Sound_DecoderInfo::author.3
mv buffer.3 Sound_Sample::buffer.3
mv buffer_size.3 Sound_Sameple::buffer_size.3
mv channels.3 Sound_AudioInfo::channels.3
mv decoder.3 Sound_Sample::decoder.3
mv description.3 Sound_DecoderInfo::description.3
mv desired.3 Sound_Sample::desired.3
mv extensions.3 Sound_DecoderInfo::extensions.3
mv flags.3 Sound_Sample::flags.3
mv format.3 Sound_AudioInfo::format.3
mv major.3 Sound_Version::major.3
mv minor.3 Sound_Version::minor.3
mv opaque.3 Sound_Sample::opaque.3
mv patch.3 Sound_Version::patch.3
mv rate.3 Sound_AudioInfo::rate.3
mv url.3 Sound_DecoderInfo::url.3
popd

mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv man3 $RPM_BUILD_ROOT/%{_mandir}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/playsound*
%{_libdir}/libSDL_sound-1.0.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/html
%{_libdir}/libSDL_sound*.so
%{_includedir}/SDL/SDL_sound.h
%{_mandir}/man3/*


%changelog
