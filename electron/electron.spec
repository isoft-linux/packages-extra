#we use prebuilt version of electron.
Name: electron
Version: 0.35.4
Release: 2 
Summary: Build cross platform desktop apps with web technologies

License: MIT
URL: http://electron.atom.io/
Source0: https://github.com/atom/electron/releases/download/v%{version}/electron-v%{version}-linux-x64.zip
Source1: electron-find-provides.sh
Source2: electron-find-requires.sh
Source10: electron.desktop
Source11: electron.svg

#filter out internal libnode.so
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

Requires: desktop-file-utils 

%description
Use HTML, CSS, and JavaScript with Chromium and Node.js to build your app.


%prep
%build
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/electron
mkdir -p %{buildroot}%{_bindir}

unzip %{SOURCE0} -d %{buildroot}%{_libdir}/electron

#link electron to /usr/bin
pushd %{buildroot}%{_bindir}
ln -sf %{_libdir}/electron/electron .
popd

#desktop file and icon
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 %{SOURCE10} %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE11} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
%{_bindir}/update-desktop-database -q &> /dev/null ||:
fi

%posttrans
%{_bindir}/update-desktop-database -q &> /dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files
%{_bindir}/electron
%dir %{_libdir}/electron
%{_libdir}/electron/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%changelog
* Thu Dec 10 2015 Cjacker <cjacker@foxmail.com> - 0.35.4-2
- Update

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.34.2-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.33.8-2
- Rebuild

* Thu Oct 15 2015 Cjacker <cjacker@foxmail.com>
- initial build.
