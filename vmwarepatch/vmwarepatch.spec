Name: vmwarepatch
Version: 0.1
Release: 2
Summary: vmware workstation 12 systemd service
License: GPL
URL: www.archlinux.org
Patch0: vmware.service
Patch1: vmware-usbarbitrator.service
Patch2: vmware-workstation-server.service
# Requires:  /etc/init.d/vmware
# Requires:  /etc/init.d/vmware-workstation-server

%description
vmware workstation 12 systemd service


%prep
echo "No prep!"

%build
echo "No build!"


%install
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/systemd/system/
install -m 644 %{PATCH0} $RPM_BUILD_ROOT%{_libdir}/systemd/system/
install -m 644 %{PATCH1} $RPM_BUILD_ROOT%{_libdir}/systemd/system/
install -m 644 %{PATCH2} $RPM_BUILD_ROOT%{_libdir}/systemd/system/

%post
systemctl enable vmware.service vmware-usbarbitrator.service
if [ -f /etc/init.d/vmware ]; then
    systemctl start vmware.service vmware-usbarbitrator.service \
|| echo "Please make sure you install vmware, and use it after reboot!"
fi

%files
%{_libdir}/systemd/system/vmware.service
%{_libdir}/systemd/system/vmware-usbarbitrator.service
%{_libdir}/systemd/system/vmware-workstation-server.service

%changelog
* Fri Dec 25 2015 sulit <sulitsrc@gmail.com> - 0.1-2
- Init for isoft4.
