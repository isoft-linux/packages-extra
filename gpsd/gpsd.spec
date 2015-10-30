Name: gpsd
Version: 3.15
Release: 3
Summary: Service daemon for mediating access to a GPS

License: BSD
URL: http://catb.org/gpsd/
Source0: http://download.savannah.gnu.org/releases/gpsd/%{name}-%{version}.tar.gz
Source11: gpsd.sysconfig

Patch0: gpsd-dirty-hack-to-fix-build.patch

BuildRequires: dbus-devel dbus-glib-devel ncurses-devel xmlto python-devel
BuildRequires: scons desktop-file-utils bluez-libs-devel pps-tools-devel
BuildRequires: libusb-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: udev
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description 
gpsd is a service daemon that mediates access to a GPS sensor
connected to the host computer by serial or USB interface, making its
data on the location/course/velocity of the sensor available to be
queried on TCP port 2947 of the host computer.  With gpsd, multiple
GPS client applications (such as navigational and wardriving software)
can share access to a GPS without contention or loss of data.  Also,
gpsd responds to queries with a format that is substantially easier to
parse than NMEA 0183.  

%package libs
Summary: Client libraries in C and Python for talking to a running gpsd or GPS

%description libs
This package contains the gpsd libraries and python modules that manage access
to a GPS for applications.

%package devel
Summary: Development files for the gpsd library
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides C header files and python modules for the gpsd shared 
libraries that manage access to a GPS for applications

%package clients
Summary: Clients for gpsd

%description clients
xgps is a simple test client for gpsd with an X interface. It displays
current GPS position/time/velocity information and (for GPSes that
support the feature) the locations of accessible satellites.

xgpsspeed is a speedometer that uses position information from the GPS.
It accepts an -h option and optional argument as for gps, or a -v option
to dump the package version and exit. Additionally, it accepts -rv
(reverse video) and -nc (needle color) options.

cgps resembles xgps, but without the pictorial satellite display.  It
can run on a serial terminal or terminal emulator.


%prep
%setup -q
%patch0 -p1

# set gpsd revision string to include package revision
sed -i 's|^revision=.*REVISION.*$|revision='\'\
'#define REVISION "%{version}-%{release}'\"\'\| SConstruct

# fix systemd path
sed -i 's|systemd_dir =.*|systemd_dir = '\'%{_unitdir}\''|' SConstruct

# don't set RPATH
sed -i 's|env.Prepend.*RPATH.*|pass #\0|' SConstruct

%build

export CCFLAGS="%{optflags}"
# breaks with %{_smp_mflags}
scons \
	dbus_export=yes \
	systemd=yes \
	libQgpsmm=no \
	debug=yes \
	leapfetch=no \
	prefix="" \
	sysconfdif=%{_sysconfdir} \
	bindir=%{_bindir} \
	includedir=%{_includedir} \
	libdir=%{_libdir} \
	sbindir=%{_sbindir} \
	mandir=%{_mandir} \
	docdir=%{_docdir} \
	pkgconfigdir=%{_libdir}/pkgconfig \
	udevdir=$(dirname %{_udevrulesdir}) \
	build


%install
# avoid rebuilding
export CCFLAGS="%{optflags}"
DESTDIR=%{buildroot} scons install systemd_install udev-install

# use the old name for udev rules
mv %{buildroot}%{_udevrulesdir}/{25,99}-gpsd.rules

%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 0644 %{SOURCE11} \
	%{buildroot}%{_sysconfdir}/sysconfig/gpsd


# Install logo icon for .desktop files
%{__install} -d -m 0755 %{buildroot}%{_datadir}/gpsd
%{__install} -p -m 0644 packaging/X11/gpsd-logo.png %{buildroot}%{_datadir}/gpsd/gpsd-logo.png

# Missed in scons install 
%{__install} -p -m 0755 gpsinit %{buildroot}%{_sbindir}

# Not needed since gpsd.h is not installed
rm %{buildroot}%{_libdir}/pkgconfig/libgpsd.pc

%post
%systemd_post gpsd.service gpsd.socket

%preun
%systemd_preun gpsd.service gpsd.socket

%postun
# Don't restart the service
%systemd_postun

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc README COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/gpsd
%{_sbindir}/gpsdctl
%{_sbindir}/gpsinit
%{_bindir}/gpsprof
%{_bindir}/gpsmon
%{_bindir}/gpsctl
%{_bindir}/ntpshmmon
%{_unitdir}/gpsd.service
%{_unitdir}/gpsd.socket
%{_unitdir}/gpsdctl@.service
%{_udevrulesdir}/*.rules
%{_mandir}/man8/gpsd.8*
%{_mandir}/man8/gpsdctl.8*
%{_mandir}/man8/gpsinit.8*
%{_mandir}/man1/gpsprof.1*
%{_mandir}/man1/gpsmon.1*
%{_mandir}/man1/gpsctl.1*
%{_mandir}/man1/ntpshmmon.1*

%files libs
%{_libdir}/libgps.so.22*
%{python_sitearch}/gps*
%exclude %{python_sitearch}/gps/fake*

%files devel
%doc TODO
%{_bindir}/gpsfake
%{_libdir}/libgps.so
%{_libdir}/pkgconfig/libgps.pc
%{python_sitearch}/gps/fake*
%{_includedir}/gps.h
%{_includedir}/libgpsmm.h
%{_mandir}/man1/gpsfake.1*
%{_mandir}/man3/libgps.3*
%{_mandir}/man3/libQgpsmm.3*
%{_mandir}/man3/libgpsmm.3*
%{_mandir}/man5/gpsd_json.5*
%{_mandir}/man5/srec.5*

%files clients
%{_bindir}/cgps
%{_bindir}/gegps
%{_bindir}/gps2udp
%{_bindir}/gpscat
%{_bindir}/gpsdecode
%{_bindir}/gpspipe
%{_bindir}/gpxlogger
%{_bindir}/lcdgps
%{_bindir}/xgps
%{_bindir}/xgpsspeed
%{_mandir}/man1/gegps.1*
%{_mandir}/man1/gps.1*
%{_mandir}/man1/gps2udp.1*
%{_mandir}/man1/gpsdecode.1*
%{_mandir}/man1/gpspipe.1*
%{_mandir}/man1/lcdgps.1*
%{_mandir}/man1/xgps.1*
%{_mandir}/man1/xgpsspeed.1*
%{_mandir}/man1/cgps.1*
%{_mandir}/man1/gpscat.1*
#%{_datadir}/applications/*.desktop
%dir %{_datadir}/gpsd
%{_datadir}/gpsd/gpsd-logo.png


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.15-3
- Rebuild

