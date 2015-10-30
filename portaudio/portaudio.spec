Name:           portaudio
Version:        19
Release:        21%{?dist}
Summary:        Free, cross platform, open-source, audio I/O library
License:        MIT
URL:            http://www.portaudio.com/
Source0:        http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
Patch1:         portaudio-doxynodate.patch
Patch2:         portaudio-pkgconfig-alsa.patch
# Add some extra API needed by audacity
# http://audacity.googlecode.com/svn/audacity-src/trunk/lib-src/portmixer/portaudio.patch
Patch3:         portaudio-audacity.patch
BuildRequires:  doxygen
BuildRequires:  alsa-lib-devel
BuildRequires:  libtool

%description
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.


%package devel
Summary:        Development files for the portaudio audio I/O library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
PortAudio is a portable audio I/O library designed for cross-platform
support of audio. It uses a callback mechanism to request audio processing.
Audio can be generated in various formats, including 32 bit floating point,
and will be converted to the native format internally.

This package contains files required to build applications that will use the
portaudio library.


%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Needed for patch3
autoreconf -i -f


%build
%configure --disable-static --enable-cxx
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' bindings/cpp/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' bindings/cpp/libtool
# no -j# because building with -j# is broken
make
# Build html devel documentation
doxygen


%install
%make_install


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc LICENSE.txt README.txt
%{_libdir}/*.so.*

%files devel
%doc doc/html/*
%{_includedir}/portaudiocpp/
%{_includedir}/portaudio.h
%{_includedir}/pa_linux_alsa.h
%{_includedir}/pa_unix_oss.h
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 19-21
- Initial build

