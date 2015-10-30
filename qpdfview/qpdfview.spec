Name:		qpdfview
Version:	0.4.15
Release:	2%{?dist}
License:	GPLv2+
Summary:	Tabbed PDF Viewer
Url:		https://launchpad.net/qpdfview
Source0:	https://launchpad.net/qpdfview/trunk/%{version}/+download/%{name}-%{version}.tar.gz
BuildRequires:	desktop-file-utils file-devel cups-devel 
BuildRequires:  hicolor-icon-theme pkgconfig(poppler-qt5) 
BuildRequires:  pkgconfig(libspectre) pkgconfig(zlib)
BuildRequires:	pkgconfig(ddjvuapi)

%description
qpdfview is a tabbed PDF viewer.
It uses the Poppler library for rendering and CUPS for printing.
It provides a clear and simple graphical user interface using the Qt framework.


%prep
%setup0 -q


%build
lrelease-qt5 qpdfview.pro
qmake-qt5 \
    QMAKE_CFLAGS+="%{optflags}" \
    QMAKE_CXXFLAGS+="%{optflags}" \
    QMAKE_STRIP="" \
    PLUGIN_INSTALL_PATH="%{_libdir}/%{name}" \
    DATA_INSTALLPATH="%{_datadir}/%{name}" \
    qpdfview.pro
make %{?_smp_mflags}

%install
make INSTALL_ROOT=%{buildroot} install
install -Dm 0644 icons/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %{name} --with-qt --without-mo
# unknown language
rm -f %{buildroot}/%{_datadir}/%{name}/%{name}_ast.qm


%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig


%files -f %{name}.lang
%doc CHANGES CONTRIBUTORS COPYING README TODO
%{_bindir}/%{name}
%{_libdir}/%{name}/
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/help*.html
#{_datadir}/%{name}/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man?/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.4.15-2
- Rebuild

