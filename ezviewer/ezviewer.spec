Name: ezviewer 
Version: 3.4
Release: 5.git
Summary: The default image viewer

License: GPLv2
URL: https://github.com/yuezhao/ezviewer
#git clone https://github.com/yuezhao/ezviewer.git
Source0: ezviewer.tar.xz
Source1: ezviewer.desktop
Patch0: ezviewer-isoft-customized.patch

BuildRequires: qt5-qtbase-devel	

%description
%{summary}

%prep
%setup -q -n %{name}
%patch0 -p1

%build
qmake-qt5
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0755 ezviewer %{buildroot}%{_bindir}/
install -m 0644 %{SOURCE1}  %{buildroot}%{_datadir}/applications/

%files
%{_bindir}/ezviewer
%{_datadir}/applications/ezviewer.desktop

%changelog
* Sun Oct 25 2015 Cjacker <cjacker@foxmail.com> - 3.4-5.git
- Rebuild for new 4.0 release

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- initial build.
- add image/webp, image/x-icns to desktop file.
