Name:           qwx
Summary:        WeChat for linux
Version:        0.9.0
Release:        1
License:        GPL-3.0
Url:            https://github.com/xiangzhai/qwx

Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.desktop
Source2:        %{name}.png

BuildRequires:  cmake
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtquickcontrols-devel

%description
WeChat for linux, base with QT5.

%prep
%setup -q 
chmod 644 LICENSE

%build
mkdir %{_target_platform}
pushd %{_target_platform}
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}    \
    -DCMAKE_BUILD_TYPE=Release ..
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
install -m644 -p -D %{SOURCE1} %{buildroot}%{_prefix}/share/applications/%{name}.desktop
install -m644 -p -D %{SOURCE2} %{buildroot}%{_prefix}/share/icons/%{name}.png
make install DESTDIR=%{buildroot} -C %{_target_platform}

%files 
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png
%{_bindir}/%{name}

%changelog
* Wed Nov 30 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 0.9.0-1
- 0.9.0-1

* Fri Dec 11 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Release v0.7

* Thu Nov 26 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Release 0.6.0
