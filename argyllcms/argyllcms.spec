Name:    argyllcms
Version: 1.8.2
Release: 2%{?dist}
Summary: ICC compatible color management system
License: GPLv3 and MIT
URL:     http://gitorious.org/hargyllcms
Source0: http://people.freedesktop.org/~hughsient/releases/hargyllcms-%{version}.tar.xz

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: libtiff-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libusb1-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: automake
BuildRequires: zlib-devel

%description
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

Spectral sample data is supported, allowing a selection of illuminants observer
types, and paper fluorescent whitener additive compensation. Profiles can also
incorporate source specific gamut mappings for perceptual and saturation
intents. Gamut mapping and profile linking uses the CIECAM02 appearance model,
a unique gamut mapping algorithm, and a wide selection of rendering intents. It
also includes code for the fastest portable 8 bit raster color conversion
engine available anywhere, as well as support for fast, fully accurate 16 bit
conversion. Device color gamuts can also be viewed and compared using a VRML
viewer.

%package doc
Summary: Argyll CMS documentation
# Does not really make sense without Argyll CMS itself
Requires: %{name} = %{version}-%{release}

%description doc
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

This package contains the Argyll color management system documentation.

%prep
%setup -q -n hargyllcms-%{version}
# we're not allowed to refer to acquisition devices as scanners
./legal.sh
autoreconf --force --install

%build
%configure --disable-static
make

%install
make install DESTDIR=%{buildroot}

# We don't want other programs to use these
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so

# rely on colord  to provide ENV{COLOR_MEASUREMENT_DEVICE}="1"
rm -f $RPM_BUILD_ROOT/lib/udev/rules.d/55-Argyll.rules

%files
%defattr(0644,root,root,0755)
%doc *.txt

%attr(0755,root,root) %{_bindir}/*
%{_datadir}/color/argyll
%{_datadir}/color/argyll/ref
%{_libdir}/lib*.so.*

%exclude %{_datadir}/doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files doc
%defattr(0644,root,root,0755)
%doc doc/*.html doc/*.jpg doc/*.txt

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.8.2-2
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
