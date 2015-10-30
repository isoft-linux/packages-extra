Name:		openbox
Version:	3.6
Release:    6 
Summary:	A highly configurable and standards-compliant X11 window manager

License:	GPLv2+
URL:		http://www.openbox.org
Source0:	http://icculus.org/openbox/releases/%{name}-%{version}.tar.gz
Source1:	http://icculus.org/openbox/tools/setlayout.c
Source4:    openbox-rc.xml
Source5:    openbox-menu.xml
Source6:    mixerctl.c
Source7:    toggle-dpms_ss
Source8:    autostart.sh
Patch0:     openbox-fix-gtk3-crash.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-xdg
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	pango-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXt-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXinerama-devel

%description
Openbox is a window manager designed explicity for standards-compliance and
speed. It is fast, lightweight, and heavily configurable (using XML for its
configuration data). It has many features that make it unique among window
managers: window resistance, chainable key bindings, customizable mouse
actions, multi-head/Xinerama support, and dynamically generated "pipe menus."

For a full list of the FreeDesktop.org standards with which it is compliant,
please see the COMPLIANCE file in the included documentation of this package. 
For a graphical configuration editor, you'll need to install the obconf
package. For a graphical menu editor, you'll need to install the obmenu
package.


%package	devel
Summary:	Development files for %{name}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig
Requires:	pango-devel
Requires:	libxml2-devel
Requires:	glib2-devel

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package	libs
Summary:	Shared libraries for %{name}

%description	libs
The %{name}-libs package contains shared libraries used by %{name}.


%prep
%setup -q
%patch0 -p1
%build
%configure \
	--disable-static \
    --disable-imlib2
## Fix RPATH hardcoding.
sed -ie 's|^hardcode_libdir_flag_spec=.*$|hardcode_libdir_flag_spec=""|g' libtool
sed -ie 's|^runpath_var=LD_RUN_PATH$|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

gcc %{optflags} -o setlayout %{SOURCE1} -lX11

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install setlayout %{buildroot}%{_bindir}

%find_lang %{name}
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_datadir}/doc/%{name}


mkdir -p $RPM_BUILD_ROOT/etc/xdg/openbox
install -D -m0644 %{SOURCE4} -C $RPM_BUILD_ROOT/etc/xdg/openbox/rc.xml
install -D -m0644 %{SOURCE5} -C $RPM_BUILD_ROOT/etc/xdg/openbox/menu.xml

gcc -o mixerctl %{SOURCE6} -lasound
install -m 0755 mixerctl $RPM_BUILD_ROOT/usr/bin
install -m 0755 %{SOURCE7} $RPM_BUILD_ROOT/usr/bin

rm -rf $RPM_BUILD_ROOT/etc/xdg/openbox/autostart
install -m 0755 %{SOURCE8} $RPM_BUILD_ROOT/etc/xdg/openbox/autostart
%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG COMPLIANCE COPYING README
%doc data/*.xsd data/menu.xml doc/rc-mouse-focus.xml
%dir %{_sysconfdir}/xdg/%{name}/
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_bindir}/gnome-panel-control
%{_bindir}/gdm-control
%{_bindir}/%{name}*
%{_bindir}/setlayout
%{_bindir}/obxprop
%{_datadir}/applications/*%{name}.desktop
#%{_datadir}/%{name}
%{_datadir}/themes/*/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/gnome/wm-properties/
%{_datadir}/xsessions/%{name}*.desktop
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/obxprop*.1*
%{_bindir}/mixerctl
%{_bindir}/toggle-dpms_ss
%{_libexecdir}/*
%files	libs
%{_libdir}/libobrender.so.*
%{_libdir}/libobt.so.*

%files	devel
%{_includedir}/%{name}/
%{_libdir}/libobrender.so
%{_libdir}/libobt.so
%{_libdir}/pkgconfig/*.pc
%post
echo "DISPLAYMANAGER=slim" > /etc/sysconfig/desktop
echo "DESKTOP=OPENBOX" >>/etc/sysconfig/desktop

%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.6-6
- Rebuild

