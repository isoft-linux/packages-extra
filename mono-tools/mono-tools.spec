Name:           mono-tools
Version:        3.10 
Release:        5 
Summary:        Mono Development Tools 

License:        LGPL
Source0:        %{name}-%{version}.tar.gz
Patch0:         mono-tools-fix-with-sdk4.patch
Patch1:         mono-tools-remove-non-exist-files-in-webdoc-makefile.patch
Patch2:         mono-tools-default-to-dmcs.patch

BuildRequires:  mono-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-sharp
BuildRequires:  gtk2-webkit-sharp-devel
Requires:	gtk2-sharp
Requires:   gtk2-webkit-sharp

#API documents is always in devel package
Requires:   mono-devel

BuildArch:noarch
%description
Mono Development Tools 

%prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./autogen.sh
GMCS=/usr/bin/dmcs %configure
make 

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps
cp $RPM_BUILD_ROOT/usr/share/pixmaps/gendarme.svg $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps/


%find_lang mono-tools

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database ||:

%postun
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database ||:

%files -f mono-tools.lang
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_libdir}/create-native-map
%{_libdir}/create-native-map/*
%dir %{_libdir}/gendarme
%{_libdir}/gendarme/*
%dir %{_libdir}/gsharp
%{_libdir}/gsharp/*
%dir %{_libdir}/gui-compare
%{_libdir}/gui-compare/*
%dir %{_libdir}/ilcontrast
%{_libdir}/ilcontrast/*
%dir %{_libdir}/minvoke
%{_libdir}/minvoke/*
%dir %{_libdir}/mono-tools
%{_libdir}/mono-tools/*
%dir %{_libdir}/mperfmon
%{_libdir}/mperfmon/*
%{_libdir}/monodoc/MonoWebBrowserHtmlRender.dll
%{_libdir}/monodoc/WebKitHtmlRender.dll
%{_libdir}/monodoc/browser.exe
%{_libdir}/monodoc/sources/*
%{_libdir}/monodoc/web/*

%{_libdir}/pkgconfig/*.pc

%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*

%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/pixmaps/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.10-5
- Rebuild

