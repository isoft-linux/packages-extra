Name:		SDL_mixer
Version:	1.2.12
Release: 	3
Summary:	Simple DirectMedia Layer - Sample Mixer Library

Group:		System Environment/Libraries
License:	LGPLv2
URL:		http://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz

Patch0:         SDL_mixer-MikMod-1.patch
Patch1:         SDL_mixer-MikMod-2.patch

BuildRequires:	SDL-devel >= 1.2.10 
BuildRequires:	libvorbis-devel
Requires:	libvorbis

%description
A simple multi-channel audio mixer for SDL. It supports 4 channels of
16 bit stereo audio, plus a single channel of music, mixed by the popular
MikMod MOD, Timidity MIDI and Ogg Vorbis libraries.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.10
Requires:	libvorbis-devel
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
    --disable-dependency-tracking	\
    --disable-static 			\
    --disable-music-libmikmod

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall install-bin

#to avoid conflicts with SDL2_mixer
mv %{buildroot}%{_bindir}/playmus  %{buildroot}%{_bindir}/playmus-1
mv %{buildroot}%{_bindir}/playwave %{buildroot}%{_bindir}/playwave-1


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING
%{_bindir}/playmus-1
%{_bindir}/playwave-1
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/SDL

%changelog
* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- rename binary to avoid conflicts with SDL2_mixer

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

