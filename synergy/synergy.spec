Summary: Share mouse and keyboard between multiple computers over the network
Name: synergy
Version: 1.6.2
Release: 3
License: GPLv2
URL: http://synergy-foss.org/
Source: https://github.com/synergy/synergy/archive/%{version}.tar.gz

#http://synergy-project.org/spit/issues/details/3567/
Patch0: synergy-1.5.0-unbundle_cryptopp.patch

#Don't override build flags
Patch1: synergy-1.5.0-flags.patch

# Last built version of synergy-plus was 1.3.4-12.fc20
Provides: synergy-plus = %{version}-%{release}
Obsoletes: synergy-plus < 1.3.4-13
BuildRequires: cmake
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
BuildRequires: libXinerama-devel
BuildRequires: qt4-devel
BuildRequires: libcurl-devel
BuildRequires: unzip
#BuildRequires: cryptopp-devel
BuildRequires: desktop-file-utils
BuildRequires: avahi-compat-libdns_sd-devel

%description
Synergy lets you easily share your mouse and keyboard between multiple
computers, where each computer has its own display. No special hardware is
required, all you need is a local area network. Synergy is supported on
Windows, Mac OS X and Linux. Redirecting the mouse and keyboard is as simple
as moving the mouse off the edge of your screen.

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1
%patch1 -p1
unzip ext/cryptopp562.zip -d ext/cryptopp562
rm -f ext/gmock-1.6.0.zip
rm -f ext/gtest-1.6.0.zip
rm -rf src/test
#Disable tests for now (bundled gmock/gtest)
sed -i /.*\(test.*/d src/CMakeLists.txt

%build
PATH="$PATH:/usr/lib64/qt4/bin:/usr/lib/qt4/bin"
%{cmake} .
make %{?_smp_mflags}
pushd src/gui
%qmake_qt4 gui.pro -r
make %{?_smp_mflags}

%install
# No install target (yet? as of 1.3.7)
install -D -p -m 0755 bin/synergyc %{buildroot}%{_bindir}/synergyc
install -D -p -m 0755 bin/synergys %{buildroot}%{_bindir}/synergys
install -D -p -m 0755 bin/synergy %{buildroot}%{_bindir}/synergy
install -D -p -m 0644 doc/synergyc.man %{buildroot}%{_mandir}/man8/synergyc.8
install -D -p -m 0644 doc/synergys.man %{buildroot}%{_mandir}/man8/synergys.8
install -D -p -m 0644 res/synergy.desktop %{buildroot}%{_datadir}/applications/synergy.desktop
install -D -p -m 0644 res/synergy.ico %{buildroot}%{_datadir}/pixmaps/synergy.ico

desktop-file-install --delete-original  \
  --dir %{buildroot}%{_datadir}/applications            \
  --set-icon=%{_datadir}/pixmaps/synergy.ico            \
  %{buildroot}%{_datadir}/applications/synergy.desktop

desktop-file-validate %{buildroot}/%{_datadir}/applications/synergy.desktop

%files
# None of the documentation files are actually useful here, they all point to
# the online website, so include just one, the README
%doc COPYING README doc/synergy.conf.example*
%{_bindir}/synergyc
%{_bindir}/synergys
%{_bindir}/synergy
%{_datadir}/pixmaps/synergy.ico
%{_datadir}/applications/synergy.desktop
%{_mandir}/man8/synergyc.8*
%{_mandir}/man8/synergys.8*

%changelog
* Mon Dec 21 2015 xiaotian.wu@i-soft.com.cn - 1.6.2-3
- remove group.

* Wed Nov 25 2015 xiaotian.wu@i-soft.com.cn - 1.6.2-2
- rebuilt

* Wed Nov 25 2015 xiaotian.wu@i-soft.com.cn - 1.6.2-1
- init for isoft.
