Name: abhidhaana 
Version: 2.1
Release: 3
Summary: Williams Monier Sanskrit-English/English-Sanskrit Dictionary

License: GPL
Source0: %{name}-%{version}.tar.gz 

BuildRequires: qt5-qtbase-devel

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
qmake-qt5
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

%files
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/abhidhaana.png

%files devel
%{_includedir}/abhidhaana
%{_includedir}/libabhidhaana
%{_libdir}/libabhidhaana.a
%{_libdir}/pkgconfig/abhidhaana-plugins-1.0.pc
%{_libdir}/pkgconfig/libabhidhaana.pc

%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 2.1-3
- Rebuild

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 2.1-2
- Initial build


