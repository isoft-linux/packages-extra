Name:		SDL2_mixer
Version:	2.0.0
Release:    1 
Summary:	Simple DirectMedia Layer - Sample Mixer Library

Group:		System Environment/Libraries
License:	LGPLv2
URL:		http://www.libsdl.org/projects/SDL_mixer/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz

BuildRequires:	SDL2-devel >= 1.2.10 
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
Requires:	SDL2-devel >= 1.2.10
Requires:	libvorbis-devel
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall install-bin

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/playmus
%{_bindir}/playwave
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/SDL2

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

