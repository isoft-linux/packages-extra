Name:           usbredir
Version:        0.7
Release:        1
Summary:        USB network redirection protocol libraries
Group:          System Environment/Libraries
License:        LGPLv2+
# I've requested a fedorahosted project once that is in place these 2 should
# be updated to point there
URL:            http://cgit.freedesktop.org/~jwrdegoede/usbredir/
Source0:        http://people.fedoraproject.org/~jwrdegoede/%{name}-%{version}.tar.bz2
BuildRequires:  libusb-devel >= 1.0.9

%description
usbredir is a protocol for redirection USB traffic from a single USB device,
to a different (virtual) machine then the one to which the USB device is
attached. This package contains a number of libraries to help implementing
support for usbredir:

usbredirparser:
A library containing the parser for the usbredir protocol

usbredirhost:
A library implementing the usb-host side of a usbredir connection.
All that an application wishing to implement an usb-host needs to do is:
* Provide a libusb device handle for the device
* Provide write and read callbacks for the actual transport of usbredir data
* Monitor for usbredir and libusb read/write events and call their handlers


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        server
Summary:        Simple usb-host tcp server
Group:          System Environment/Daemons
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description    server
A simple usb-host tcp server, using libusbredirhost.


%prep
%setup -q


%build
export CC=clang
export CXX=clang++
%configure
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
  PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
make install PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING.LIB README TODO 
%{_libdir}/libusbredir*.so.*

%files devel
%defattr(-,root,root,-)
%doc usb-redirection-protocol.txt
%{_includedir}/usbredir*.h
%{_libdir}/libusbredir*.so
%{_libdir}/libusbredir*.a
%{_libdir}/pkgconfig/libusbredir*.pc

%files server
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/usbredirserver
%{_mandir}/man1/usbredirserver.1.gz


%changelog
