Name:           qwx
Summary:        WeChat for linux
Version:        0.7
Release:        1
License:        GPL-3.0
Url:            https://github.com/xiangzhai/qwx
Source:        %{name}-%{version}.tar.bz2
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtquickcontrols-devel

%description
WeChat for linux, base with QT5.

%prep
%setup -q 
chmod 644 AUTHORS.md LICENSE

%build
qmake-qt5 PREFIX=%{buildroot}%{_prefix}
make

%install
make install

%files 
%doc AUTHORS.md LICENSE
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/
%{_bindir}/%{name}

%changelog
* Fri Dec 11 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Release v0.7

* Thu Nov 26 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Release 0.6.0
