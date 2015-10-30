Summary: A version of the MIT Athena widget set for X
Name: Xaw3d
Version: 1.6.2
Release: 9%{?dist}
Source: http://xorg.freedesktop.org/archive/individual/lib/libXaw3d-%{version}.tar.bz2
Patch5: Xaw3d-1.5-debian-fixes.patch
Patch7: Xaw3d-1.6.1-3Dlabel.patch
Patch10: Xaw3d-1.6.1-fontset.patch
Patch11: Xaw3d-1.6.1-hsbar.patch

License: MIT
URL: http://xorg.freedesktop.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libXmu-devel
BuildRequires: libXt-devel
BuildRequires: libSM-devel
BuildRequires: libXext-devel
BuildRequires: libX11-devel
BuildRequires: libXpm-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: bison
BuildRequires: flex
BuildRequires: ed

%description
Xaw3d is an enhanced version of the MIT Athena Widget set for
the X Window System.  Xaw3d adds a three-dimensional look to applications
with minimal or no source code changes.

You should install Xaw3d if you are using applications which incorporate
the MIT Athena widget set and you'd like to incorporate a 3D look into
those applications.

%package devel
Summary: Header files and libraries for development using Xaw3d
Requires: %{name} = %{version}-%{release}
Requires: libXmu-devel
Requires: libXt-devel
Requires: libSM-devel
Requires: libXext-devel
Requires: libX11-devel
Requires: libXpm-devel

%description devel
Xaw3d is an enhanced version of the MIT Athena widget set for
the X Window System.  Xaw3d adds a three-dimensional look to those
applications with minimal or no source code changes. Xaw3d-devel includes
the header files and libraries for developing programs that take full
advantage of Xaw3d's features.

You should install Xaw3d-devel if you are going to develop applications
using the Xaw3d widget set.  You'll also need to install the Xaw3d
package.


%prep
%setup -q -n libXaw3d-%{version}
# This doesn't apply cleanly, but has not been applied
#%patch5 -p1 -b .debian
%patch7 -p1 -b .3Dlabel
%patch10 -p1 -b .fontset
%patch11 -p1 -b .hsbar


%build
%configure --disable-static \
  --enable-arrow-scrollbars \
  --enable-gray-stipples \
  --enable-multiplane-bitmaps
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libXaw3d.la
rm -r $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc ChangeLog COPYING README src/README.XAW3D
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/xaw3d.pc
%{_includedir}/X11/Xaw3d

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.6.2-9
- Initial build

