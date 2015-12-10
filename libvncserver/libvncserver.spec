Name: libvncserver
Version: 0.9.9
Release: 5
License: GPL

Source0: http://downloads.sourceforge.net/libvncserver/LibVNCServer-0.9.9.tar.gz
BuildRequires: libjpeg-turbo-devel gnutls-devel libgcrypt-devel

Summary:A cross-platform C libraries that allow you to easily implement VNC server
Requires: libjpeg-turbo gnutls libgcrypt

%description
A cross-platform C libraries that allow you to easily implement VNC server

%prep
%autosetup -c

%build 
cd LibVNCServer-%{version}
%{configure}
make %{?_smp_mflags}

%install
cd LibVNCServer-%{version}
make install DESTDIR=%{buildroot}

%files
%{_bindir}/libvncserver-config
%{_bindir}/linuxvnc
%{_includedir}/rfb/*.h
%{_libdir}/libvncclient.a
%{_libdir}/libvncclient.so
%{_libdir}/libvncclient.so.0
%{_libdir}/libvncclient.so.0.0.0
%{_libdir}/libvncserver.a
%{_libdir}/libvncserver.so
%{_libdir}/libvncserver.so.0
%{_libdir}/libvncserver.so.0.0.0
%{_libdir}/pkgconfig/libvncclient.pc
%{_libdir}/pkgconfig/libvncserver.pc


%changelog
* Thu Dec 10 2015 xiaotian.wu@i-soft.com.cn - 0.9.9-5
- rebuilt

* Thu Dec 10 2015 xiaotian.wu@i-soft.com.cn - 0.9.9-4
- rebuilt

