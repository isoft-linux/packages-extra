# use the follow command build the package, **DON'T USE KOJI BUILD IT**
# QA_RPATHS=$((0x0004|0x0008)) rpmbuild -ba netease-cloud-music.spec

%global	       debug_package %{nil}
Name: netease-cloud-music  
Version: 1.0.0
Release: 2
Summary: netease cloud music player.
License: netease-cloud-music-proprietary
URL:  music.163.com
Source0: netease-cloud-music_1.0.0_amd64_ubuntu16.04.deb

BuildRequires: binutils
Provides: libcef.so()(64bit)

%description
netease cloud music player.

%prep
%setup -c -T
ar -x %{SOURCE0}
tar xf control.tar.gz
tar xf data.tar.xz

%build

%install
cp -r usr %{buildroot}

%post
ldconfig

%files
%doc /usr/share/doc/netease-cloud-music/*
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/applications/netease-cloud-music.desktop
%{_datadir}/icons/hicolor/scalable/apps/netease-cloud-music.svg

%changelog
* Fri Aug 12 2016 sulit <sulitsrc@gmail.com> - 1.0.0-2
- make rpm from deb
