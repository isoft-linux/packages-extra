%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary:	Jabber client written in PyGTK
Name:		gajim
%global		majorver 0.16
#global		prever -rcX
Version:	0.16.4
Release:	5%{?dist}
License:	GPLv3
Group:		Applications/Internet
URL:		http://gajim.org/
Source0:	http://gajim.org/downloads/%{majorver}/%{name}-%{version}%{?prever}.tar.bz2
BuildArch:	noarch

Requires:	dbus-python
#  Audio/Video calls:
# Requires:	farstream-python
Requires:	gstreamer-python
# XXX: Gajim does not import bonobo directly, but some module does and
# prints an error if it's not available.
# Requires:	gnome-python2-bonobo
# Requires:	gnome-python2-desktop
# Requires:	gnome-python2-gnome
# Requires:	gupnp-igd-python
Requires:	hicolor-icon-theme
Requires:	notify-python
Requires:	pyOpenSSL
Requires:	python-avahi
Requires:	python-crypto
Requires:	python-gnupg
Requires:	python-kerberos
Requires:	python-libasyncns
Requires:	python-nbxmpp >= 0.5.3
Requires:	python-pyasn1
Requires:	python-pycurl

# these are dlopen'd using ctypes find_library/LoadLibrary:
Requires:	gtkspell
Requires:	libXScrnSaver

# Optional features with significatly sized deps. Gajim detects them at
# runtime. Intentionally not as hard deps.
# XXX: Gajim could install them using PackageKit when really necessary.
#  Password encryption:
#Requires:	gnome-python2-gnomekeyring
#  RST Generator:
#Requires:	python-docutils

BuildRequires:	python2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	hardlink

Patch0001: 0001-request-archiving-preferences-only-if-server-announc.patch
Patch0002: 0002-stop-requesting-MAM-archive-when-we-get-the-complete.patch
Patch0003: 0003-really-import-gst-when-testing-if-it-s-available-ins.patch
Patch0004: 0004-Correctly-check-and-handle-the-case-when-we-don-t-tr.patch
Patch0005: 0005-do-not-delay-the-import-of-libxml2-it-s-needed-by-gs.patch

%description
Gajim is a Jabber client written in PyGTK. The goal of Gajim's developers is
to provide a full featured and easy to use xmpp client for the GTK+ users.
Gajim does not require GNOME to run, even though it exists with it nicely.

%prep
%autosetup -p1 -n %{name}-%{version}%{?prever}

%build
%configure --docdir=%{_pkgdocdir} PYTHON=/usr/bin/python2

make %{?_smp_mflags}

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
hardlink -c $RPM_BUILD_ROOT/%{_bindir}

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category=Application \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Icon_Cache
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc README.html
%doc THANKS
%doc THANKS.artists
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{name}-history-manager.1*
%doc %{_mandir}/man1/%{name}-remote.1*
%{_bindir}/%{name}
%{_bindir}/%{name}-history-manager
%{_bindir}/%{name}-remote
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/data
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/src

%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.16.4-5
- uncomment Requires:	gstreamer-python, because koji
- repo gstreamer-python compile should use gstreamer0
- it's repaired by teacher Wu.

* Wed Dec 02 2015 sulit <sulitsrc@gmail.com> - 0.16.4-4
- Init for isoft4.0
- comment Requires:	farstream-python, because koji 
- repo farstream-python version change
- comment Requires:	gstreamer-python, because koji
- repo gstreamer-python compile don't pass, gstreamer
- version cause of it.
- the up two items related to Audio/Video calls
-
- TODO:
- comment Requires:	gupnp-igd-python, because koji
- repo gupnp-igd don't provide it, I may be modify
- gupnp-igd, if the time is enough
