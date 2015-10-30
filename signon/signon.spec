Name:           signon
Version:        8.57
Release:        8%{?dist}
Summary:        Accounts framework for Linux and POSIX based platforms

License:        LGPLv2
URL:            https://code.google.com/p/accounts-sso

# Source available from https://drive.google.com/drive/#folders/0B8fX9XOwH_g4alFsYV8tZTI4VjQ
# as per https://groups.google.com/forum/#!topic/accounts-sso-announce/8MserPgUV5M
Source0:        signon-%{version}.tar.bz2

# cmake config files still define SIGNONQT_LIBRARIES_STATIC, but meh, anyone who
# tries to use that deserves what they get
Patch1: signon-8.57-no_static.patch
Patch2: signon-fix-missing-header.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  doxygen
BuildRequires:  libproxy-devel

# signon-qt5 was in ktp-5 COPR
Obsoletes:      signon-qt5 < 8.57-5
Provides:       signon-qt5 = %{version}-%{release}

Requires:       dbus

%description
Single Sign-On is a framework for centrally storing authentication credentials
and handling authentication on behalf of applications as requested by
applications. It consists of a secure storage of login credentials (for example
usernames and passwords), plugins for different authentication systems and a
client library for applications to communicate with this system.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
The %{name}-doc package contains documentation for %{name}.


%prep
%setup -q -n signon-%{version}

%patch1 -p1 -b .no_static
%patch2 -p1

%build
# Make sure it compiles against Fedora's Qt5
sed -i "s/qdbusxml2cpp/qdbusxml2cpp-qt5/" src/signond/signond.pro

export PATH=%{_qt5_bindir}:$PATH

# FIXME: out-of-src tree build fails -- rex
qmake-qt5 signon.pro \
  CONFIG+=release \
  QMF_INSTALL_ROOT=%{_prefix} LIBDIR=%{_libdir}

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# create/own libdir/extensions
mkdir -p %{buildroot}%{_libdir}/extensions/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README TODO NOTES COPYING
%config(noreplace) %{_sysconfdir}/signond.conf
%{_bindir}/signond
%{_bindir}/signonpluginprocess
%{_libdir}/libsignon-extension.so.1*
%{_libdir}/libsignon-plugins-common.so.1*
%{_libdir}/libsignon-plugins.so.1*
%{_libdir}/libsignon-qt5.so.1*
%{_libdir}/signon/
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service

%files devel
%{_includedir}/signon-extension/
%{_includedir}/signon-plugins/
%{_includedir}/signon-qt5/
%{_includedir}/signond/
%{_libdir}/cmake/SignOnQt5/
%{_libdir}/libsignon-extension.so
%{_libdir}/libsignon-plugins-common.so
%{_libdir}/libsignon-plugins.so
%{_libdir}/libsignon-qt5.so
%{_libdir}/pkgconfig/SignOnExtension.pc
%{_libdir}/pkgconfig/libsignon-qt5.pc
%{_libdir}/pkgconfig/signon-plugins-common.pc
%{_libdir}/pkgconfig/signon-plugins.pc
%{_libdir}/pkgconfig/signond.pc

%files doc
%{_docdir}/signon/
%{_docdir}/libsignon-qt/
%{_docdir}/signon-plugins/
%{_docdir}/signon-plugins-dev/


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 8.57-8
- Rebuild

