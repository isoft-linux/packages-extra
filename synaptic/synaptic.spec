Summary: Graphical frontend for APT package manager.
Name: synaptic
Version: 0.57.2
Release: 43%{?dist}
License: GPLv2+
URL: http://www.nongnu.org/synaptic/

Source0: http://savannah.nongnu.org/download/synaptic/synaptic-%{version}.tar.gz

Patch0: synaptic-0.57-desktop.patch
Patch1: synaptic-0.57-firefox.patch

# Patches from apt-rpm maintainer for gcc 4.1 support, repomd support
# and progress meter fixes
Patch2: http://apt-rpm.org/patches/synaptic-0.57.2-gcc41.patch
Patch3: http://apt-rpm.org/patches/synaptic-0.57.2-repomd-1.patch
Patch4: http://apt-rpm.org/patches/synaptic-0.57.2-showprog.patch
Patch5: http://apt-rpm.org/patches/synaptic-0.57.2-progressapi-hack.patch
Patch6: synaptic-0.57.2-gcc43.patch
Patch7: synaptic-0.57.2-libx11.patch
Patch8: synaptic-0.57.2-gcc45.patch

Patch10: synaptic-0.57.2-drop-help-menuitem.patch
Patch11: synaptic-0.57.2-drop-help.patch

Patch12: synaptic-detect-rpm-lib-fix.patch

Requires: usermode-gtk
BuildRequires: apt-devel >= 0.5.15lorg3.92, librpm-devel >= 4.0
BuildRequires: gtk2-devel, libglade2-devel, desktop-file-utils
BuildRequires: libstdc++-devel, gettext
BuildRequires: xmlto, perl-XML-Parser

%description
Synaptic is a graphical package management
program for apt. It provides the same features as the apt-get command line
utility with a GUI front-end based on Gtk+

%prep
%setup -q
%patch0 -p1 -b .dt
%patch1 -p1 -b .firefox
%patch2 -p1 -b .gcc41
%patch3 -p1 -b .repomd
%patch4 -p1 -b .showprog
%patch5 -p1 -b .progresshack
%patch6 -p1 -b .gcc43
%patch7 -p1 -b .libx11
%patch8 -p1 -b .gcc45

%patch10 -p1
%patch11 -p1

%patch12 -p1

%build
autoreconf -ivf
intltoolize --force

#remove origial desktop ,force to re-generate.
rm -rf data/*.desktop
%configure --disable-dependency-tracking
find . -type f -exec sed -i 's:-Werror=format-security ::g' {} \;

make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/synaptic

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/synaptic
USER=root
PROGRAM=%{_sbindir}/synaptic
SESSION=true
FALLBACK=false
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/synaptic
#%PAM-1.0
auth       sufficient   /%{_lib}/security/pam_rootok.so
auth       sufficient   /%{_lib}/security/pam_timestamp.so
auth       include      system-auth
session    required     /%{_lib}/security/pam_permit.so
session    optional     /%{_lib}/security/pam_xauth.so
session    optional     /%{_lib}/security/pam_timestamp.so
account    required     /%{_lib}/security/pam_permit.so
EOF
if [ -f /%{_lib}/security/pam_stack.so ] && \
   ! grep -q "Deprecated pam_stack module" /%{_lib}/security/pam_stack.so; then
  perl -pi -e's,include(\s*)(.*),required\1pam_stack.so service=\2,' $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/synaptic
fi


%find_lang %{name}

# remove uninstalled files
rm -rf %{buildroot}/%{_localstatedir}/scrollkeeper
rm -rf %{buildroot}/%{_sysconfdir}/X11
rm -rf %{buildroot}/%{_datadir}/applications/%{name}-kde.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man8/%{name}.8*

%changelog
* Sun Nov 08 2015 Cjacker <cjacker@foxmail.com> - 0.57.2-43
- Fix librpm detection with new rpm

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.57.2-39
- Rebuild

