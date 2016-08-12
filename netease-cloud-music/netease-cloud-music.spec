# use the follow command build rpm package, **DON'T USE KOJI BUILD IT**
# QA_RPATHS=$((0x0004|0x0008)) rpmbuild -ba netease-cloud-music.spec

%global	       debug_package %{nil}
Name: netease-cloud-music  
Version: 1.0.0
Release: 1
Summary: netease cloud music player.
License: netease-cloud-music-proprietary
URL:  music.163.com
Source0: netease-cloud-music_1.0.0_amd64_ubuntu16.04.deb

BuildRequires: binutils
Provides: libcef.so()(64bit)

%description
netease cloud music player.

# %package libcef
# Summary: netease cloud music player libcef library.
# Requires: %{name}
# Provides: libcef.so()(64bit)
# 
# %description libcef
# netease cloud music player libcef library.

%prep
%setup -c -T
ar -x %{SOURCE0}
tar xf control.tar.gz
tar xf data.tar.xz

%build

%install
cp -r usr %{buildroot}

#%post #libcef
%post
ldconfig

%files
%doc /usr/share/doc/netease-cloud-music/*
%{_bindir}/%{name}
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/locales/*
%{_libdir}/%{name}/natives_blob.bin
%{_libdir}/%{name}/netease-cloud-music
%{_libdir}/%{name}/snapshot_blob.bin
%{_libdir}/%{name}/libcef.so
%{_libdir}/%{name}/cef.pak
%{_libdir}/%{name}/cef_100_percent.pak
%{_libdir}/%{name}/cef_200_percent.pak
%{_libdir}/%{name}/cef_extensions.pak
%{_datadir}/applications/netease-cloud-music.desktop
%{_datadir}/icons/hicolor/scalable/apps/netease-cloud-music.svg

# %files libcef
# %{_libdir}/%{name}/libcef.so
# %{_libdir}/%{name}/cef.pak
# %{_libdir}/%{name}/cef_100_percent.pak
# %{_libdir}/%{name}/cef_200_percent.pak
# %{_libdir}/%{name}/cef_extensions.pak

%changelog
