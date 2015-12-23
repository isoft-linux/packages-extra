%global debug_package %{nil}
Name:		virglrenderer
Version:	0.3.0
Release:	3.git

Summary:	Virgl Rendering library.
License:	MIT

# git://people.freedesktop.org/~airlied/virglrenderer
Source0:	virglrenderer.tar.gz

BuildRequires:	autoconf
BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	xorg-x11-util-macros
BuildRequires:	libepoxy-devel
BuildRequires:	mesa-libgbm-devel
BuildRequires:	mesa-libEGL-devel
BuildRequires:	python
BuildRequires:	libdrm-devel

%description
The virgil3d rendering library is a library used by
qemu to implement 3D GPU support for the virtio GPU.

%package devel
Summary: Virgil3D renderer development files

Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Virgil3D renderer development files, used by
qemu to build against.

%package test-server
Summary: Virgil3D renderer testing server

Requires: %{name}%{?_isa} = %{version}-%{release}

%description test-server
Virgil3D renderer testing server is a server
that can be used along with the mesa virgl
driver to test virgl rendering without GL.

%prep
%setup -q -n %{name}

%build
sh autogen.sh
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" install
find %{buildroot} -type f -name '*.la' | xargs rm -f -- || :

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/lib*.so.*

%files devel
%dir %{_includedir}/virgl/
%{_includedir}/virgl/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files test-server
%{_bindir}/virgl_test_server

%changelog
* Tue Dec 22 2015 Cjacker <cjacker@foxmail.com> - 0.3.0-3.git
- update

* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 0.3.0-2.git
- Initial build

