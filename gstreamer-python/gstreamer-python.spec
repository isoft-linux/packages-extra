%define         majorminor      0.10

Name:           gstreamer-python
Version:        0.10.22
Release:        10%{?dist}
Summary:        Python bindings for GStreamer

Group:          Development/Languages
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-python/gst-python-%{version}.tar.bz2
#Patch0:         gst-python-0.10.15-strayline.patch
Patch1:         0001-preset-expose-new-gst.preset_-set-get-_app_dir-on-py.patch

Requires:       python >= 2.3
Requires:       pygtk2 >= 2.8.0
Requires:       python-libxml2
Requires:       gstreamer >= 0.10.36
Requires:       gstreamer-plugins-base >= 0.10.36

BuildRequires:  python >= 2.3
BuildRequires:  python-devel >= 2.3
BuildRequires:  pygtk2-devel >= 2.8.0
# xwindowlistener needs X11 headers
BuildRequires:  libX11-devel
BuildRequires:  gstreamer-devel >= 0.10.36
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.36
BuildRequires:  pygobject2-devel >= 2.11.2


%description
This module contains a wrapper that allows GStreamer applications
to be written in Python.


%package        devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       pygtk2-devel
Requires:       gstreamer-devel


%description devel
This package contains the static libraries and header files needed for
developing gstreamer-python applications.


%prep
%setup -q -n gst-python-%{version}
%{__sed} -i 's|^#!/usr/bin/env python$|#|' gst/extend/*.py
#%patch0 -p1 -b .strayline
%patch1 -p1 -b .gst_preset_set_app_dir


%build
%configure
make %{?_smp_mflags}


%install
rm -rf docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
mkdir -p docs-to-include/examples
chmod -x examples/*.py
cp examples/*.py docs-to-include/examples/
rm -fr $RPM_BUILD_ROOT%{_datadir}/gst-python/%{majorminor}/examples


%files
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/python?.?/site-packages/gst-%{majorminor}
%{_libdir}/python?.?/site-packages/pygst.py*
%{_libdir}/python?.?/site-packages/pygst.pth
%{_libdir}/python?.?/site-packages/gstoption.so
%{_libdir}/gstreamer-0.10/*
%dir %{_datadir}/gst-python
%dir %{_datadir}/gst-python/%{majorminor}
%dir %{_datadir}/gst-python/%{majorminor}/defs
%{_datadir}/gst-python/%{majorminor}/defs/*.defs


%files devel
%doc docs-to-include/*
%{_includedir}/gstreamer-0.10/gst/pygst*.h
%{_libdir}/pkgconfig/gst-python-%{majorminor}.pc


%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.10.22-10
- Init for isoft4

