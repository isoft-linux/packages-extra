Summary:        Tool for generating configure script for qmake-based projects
Name:           qconf
Version:        1.4
Release:        3%{?dist}
Epoch:          1

Group:          Development/Tools
License:        GPLv2+ with exceptions
URL:            http://delta.affinix.com/qconf/
Source0:        http://delta.affinix.com/download/qconf-%{version}.tar.bz2

# Qt project don't support CXXFLAGS from environment. We need to use hack.
Patch0:         qconf-1.4-optflags.patch

# Fedora has gridengine package with /usr/bin/qconf
# So I need to use another name
Patch1:         qconf-1.4-rename-binary.patch

Buildrequires:  qt4-devel >= 4.4.0
# or pkgconfig-style
#BuildRequires: pkgconfig(QtXml) >= 4.4.0
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
QConf allows you to have a nice configure script for your
qmake-based project. It is intended for developers who don't need
(or want) to use the more complex GNU autotools. With qconf/qmake,
it is easy to maintain a cross-platform project that uses a
familiar configuration interface on unix.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{_qt4_qmake} PREFIX=%{_prefix}   \
              BINDIR=%{_bindir}   \
              DATADIR=%{_datadir} \
              QTDIR=%{_libdir}/qt4 \
              CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install


%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/qconf-qt4
%{_datadir}/%{name}


%changelog
* Wed Dec 02 2015 sulit <sulitsrc@gmail.com> - 1:1.4-3
- rebuilt
