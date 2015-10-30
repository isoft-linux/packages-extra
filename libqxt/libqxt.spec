Name:		libqxt
Version:	0.6.2
Release:	10%{?dist}
Summary:	Qt extension library
License:	CPL or LGPLv2
URL:		http://www.libqxt.org/
Source0:	http://bitbucket.org/libqxt/libqxt/get/v%{version}.tar.bz2
# Fix DSO linking
Patch0:		libqxt-linking.patch
# To support multimedia keys when using clementine
# Patch sent to upstream. They want to reimplement it more cleanly.
# We will use this patch until upstream reimplements it.
# http://dev.libqxt.org/libqxt/issue/75
Patch1:		libqxt-media-keys.patch
# Fix wrong header includes RHBZ#733222
# http://dev.libqxt.org/libqxt/issue/112/wrong-include-in-qxtnetworkh
Patch2:		libqxt-header-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	avahi-devel
BuildRequires:	libXrandr-devel
BuildRequires:	openssl-devel
BuildRequires:	qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
LibQxt, an extension library for Qt, provides a suite of cross-platform
utility classes to add functionality not readily available in the Qt toolkit.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-compat-libdns_sd-devel
Requires:	avahi-devel
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use LibQxt.


%prep
%setup -q -n %{name}-%{name}-v%{version}
%patch0 -p1 -b .linking
%patch1 -p1 -b .mediakeys
%patch2 -p1 -b .includes

# We don't want rpath
sed -i '/RPATH/d' src/qxtlibs.pri


%build
# Does not use GNU configure
./configure -verbose \
	    -qmake-bin qmake-qt4 \
	    -prefix %{_prefix} \
	    -libdir %{_libdir}
make %{?_smp_mflags}
make %{?_smp_mflags} docs


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# We are installing these to the proper location
rm -fr $RPM_BUILD_ROOT%{_prefix}/doc/

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES *.txt LICENSE README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/ doc/html/
%{_includedir}/*
%{_libdir}/*.so
%{_qt4_plugindir}/designer/*.so
%{_qt4_datadir}/mkspecs/features/qxt*.prf

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.6.2-10
- Rebuild

