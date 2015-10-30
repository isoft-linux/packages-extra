Name:       qterm
Version:    0.5.12
Release:    13%{?dist}
Summary:    BBS client for X Window System written in Qt
License:    GPLv2+
URL:        http://qterm.sourceforge.net/wiki/index.php/Main_Page
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# README from debian
Source1:    README.Debian
# Use the new find_package syntax introduced in CMake 2.6 to workaround a problem with Find_Qt4 shipped with KDE.
# applied in upstream svn1311
Patch0:     qterm-0.5.12-cmake.patch
# Fix build with gcc 4.7, include the missed unistd.h include
# https://sourceforge.net/tracker/?func=detail&aid=3474368&group_id=79581&atid=557094
Patch1:     qterm-0.5.12-gcc-4.7.patch
Patch2: qterm-fix-cmake-error.patch

BuildRequires:  phonon-devel
BuildRequires:  openssl-devel
BuildRequires:  qtscriptbindings
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
Requires:   hicolor-icon-theme
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}


%description
QTerm is a BBS client for X Window System. It supports Telnet, SSH1 and SSH2
protocols. It also supports ZMODEM, URL analysis and mouse gesture.

It also supports detecting location from IP address, but you need do some
extra work, see %{_docdir}/%{name}/README.package.

%prep
%setup -q
%patch0 -p2
%patch1 -p0
%patch2 -p1

%build
mkdir build
pushd build
export PATH=%{_qt4_bindir}:$PATH
%cmake -DQT_PHONON_INCLUDE_DIR:PATH=%{_includedir}/KDE ..
make %{?_smp_mflags}
popd

%install
make install/fast DESTDIR=%{buildroot} -C build

desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    --remove-category Application \
    --add-category RemoteAccess \
    %buildroot%{_datadir}/applications/*.desktop

# rename the executable to QTerm to prevent conflict with torque-client
mv %buildroot%{_bindir}/{qterm,QTerm}
sed -i 's/Exec=qterm/Exec=QTerm/' %buildroot%{_datadir}/applications/%{name}.desktop

cp -p %{SOURCE1} README.package


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README* TODO doc/*
%{_bindir}/QTerm
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.5.12-13
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 0.5.12-12
- Initial build

