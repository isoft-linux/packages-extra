Name:           sysprof
Version:        1.2.0
Release:        2 
Summary:        A system-wide Linux profiler
License:        GPLv2+
URL:            http://www.sysprof.com
Source0:        http://www.sysprof.com/sysprof-%{version}.tar.gz

Source1:        sysprof.desktop

BuildRequires:  binutils-devel
BuildRequires:  gtk2-devel
BuildRequires:  libglade2-devel

Requires:       usermode
Requires:       usermode-gtk

Requires:       kernel => 2.6.31

ExclusiveArch:  %{ix86} x86_64

%description
Sysprof is a sampling CPU profiler for Linux that collects accurate,
high-precision data and provides efficient access to the sampled
calltrees.


%prep
%setup -q -n sysprof-%{version}

%build
%configure
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

#install desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications/

#correct icons installation
for i in 16 24 32 48
do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps
    mv %{buildroot}%{_datadir}/pixmaps/sysprof-icon-$i.png %{buildroot}%{_datadir}/icons/hicolor/$i"x"$i/apps/sysprof.png
done
rm -rf %{buildroot}%{_datadir}/pixmaps


#give it root permission
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/sysprof $RPM_BUILD_ROOT%{_sbindir}/sysprof
mv $RPM_BUILD_ROOT%{_bindir}/sysprof-cli $RPM_BUILD_ROOT%{_sbindir}/sysprof-cli

ln -s consolehelper-gtk $RPM_BUILD_ROOT%{_bindir}/sysprof
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/sysprof-cli

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/sysprof
USER=root
PROGRAM=%{_sbindir}/sysprof
SESSION=true
FALLBACK=false
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sysprof
#%PAM-1.0
auth       sufficient   /%{_lib}/security/pam_rootok.so
auth       sufficient   /%{_lib}/security/pam_timestamp.so
auth       include      system-auth
session    required     /%{_lib}/security/pam_permit.so
session    optional     /%{_lib}/security/pam_xauth.so
session    optional     /%{_lib}/security/pam_timestamp.so
account    required     /%{_lib}/security/pam_permit.so
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/sysprof-cli
USER=root
PROGRAM=%{_sbindir}/sysprof-cli
SESSION=true
FALLBACK=false
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/sysprof-cli
#%PAM-1.0
auth       sufficient   /%{_lib}/security/pam_rootok.so
auth       sufficient   /%{_lib}/security/pam_timestamp.so
auth       include      system-auth
session    required     /%{_lib}/security/pam_permit.so
session    optional     /%{_lib}/security/pam_xauth.so
session    optional     /%{_lib}/security/pam_timestamp.so
account    required     /%{_lib}/security/pam_permit.so
EOF



%clean
rm -rf ${RPM_BUILD_ROOT}


%post
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q > /dev/null ||:



%files
%defattr(-,root,root,-)
%{_sysconfdir}/pam.d/sysprof
%{_sysconfdir}/pam.d/sysprof-cli
%{_sysconfdir}/security/console.apps/sysprof
%{_sysconfdir}/security/console.apps/sysprof-cli
%{_sysconfdir}/udev/rules.d/60-sysprof.rules
%{_sbindir}/sysprof-cli
%{_sbindir}/sysprof
%{_bindir}/sysprof-cli
%{_bindir}/sysprof
%{_datadir}/icons/hicolor/*/apps/sysprof.*
%{_datadir}/sysprof/sysprof.glade
%{_datadir}/applications/sysprof.desktop

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.2.0-2
- Rebuild

