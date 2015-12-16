%define _python_bytecompile_errors_terminate_build 0

Name: youdao-dict 
Version: 1.0.2
Release: 2
Summary: Youdao dictionary 

License: Commercial
URL: http://cidian.youdao.com/index-linux.html
Source0: youdao-dict_1.0.2-ubuntu_amd64.deb

BuildRequires: dpkg
%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}
dpkg --extract %{SOURCE0}  %{buildroot}

%files
%{_sysconfdir}/xdg/autostart/youdao-dict-autostart.desktop
%{_bindir}/youdao-dict
%{_datadir}/applications/youdao-dict.desktop
%{_datadir}/dbus-1/services/com.youdao.backend.service
%{_datadir}/dbus-1/services/com.youdao.indicator.service
%{_docdir}/youdao-dict
%{_datadir}/icons/hicolor/*/apps/youdao-dict.*
%dir %{_datadir}/youdao-dict
%{_datadir}/youdao-dict/*

%changelog
* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 1.0.2-2
- Initial build


