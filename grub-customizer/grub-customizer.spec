Name:           grub-customizer
Version:        4.0.6
Release:        5%{?dist}
Summary:        Graphical GRUB2 settings manager

License:        GPLv3
URL:            https://launchpad.net/grub-customizer
Source0:        https://launchpad.net/grub-customizer/4.0/%{version}/+download/%{name}_%{version}.tar.gz
Source1:        grub.cfg

BuildRequires:  cmake
BuildRequires:  gtkmm-devel
BuildRequires:  gettext
BuildRequires:  openssl-devel
BuildRequires:  libarchive-devel
BuildRequires:  desktop-file-utils

Requires:       grub

ExcludeArch:    %{arm}

%description
Grub Customizer is a graphical interface to configure the grub/burg settings
with focus on the individual list order - without losing the dynamical behavior
of grub.

The goal of this project is to create a complete and intuitive graphical
grub/burg configuration interface. The main feature is the boot entry list
configuration - but not simply by modified the grub.cfg: to keep the dynamical
configuration, this application will only edit the script order and generate
proxies (script output filter), if required.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}


%install
%make_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/grub.cfg

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc README COPYING changelog
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/grubcfg-proxy
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/polkit-1/actions/net.launchpad.danielrichter2007.pkexec.grub-customizer.policy


%changelog
