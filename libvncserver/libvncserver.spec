Name: Libvncserver
Version: 0.9.9
Release: 6
License: GPL

Source0: http://downloads.sourceforge.net/libvncserver/LibVNCServer-0.9.9.tar.gz
BuildRequires: libjpeg-turbo-devel gnutls-devel libgcrypt-devel

Summary: a library to make writing a vnc server easy
Requires: libjpeg-turbo gnutls libgcrypt

%description
LibVNCServer makes writing a VNC server (or more correctly, a program
exporting a framebuffer via the Remote Frame Buffer protocol) easy.

It is based on OSXvnc, which in turn is based on the original Xvnc by
ORL, later AT&T research labs in UK.

It hides the programmer from the tedious task of managing clients and
compression schemata.

LibVNCServer was put together and is (actively ;-) maintained by
Johannes Schindelin <Johannes.Schindelin@gmx.de>

%package      devel
Summary:      Static Libraries and Header Files for LibVNCServer
Requires:     %{name}%{?_isa} = %{version}-%{release}

%description    devel
Static Libraries and Header Files for LibVNCServer.

%prep
%autosetup -c

%build 
cd LibVNCServer-%{version}
%{configure}
make %{?_smp_mflags}

%install
cd LibVNCServer-%{version}
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre
%post
%preun
%postun

%files
%defattr(-,root,root)
%{_bindir}/linuxvnc
%{_libdir}/libvncclient.so.*
%{_libdir}/libvncserver.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/libvncserver-config
%{_includedir}/rfb/*.h
%{_libdir}/libvncclient.so
%{_libdir}/libvncserver.so
%{_libdir}/pkgconfig/libvncclient.pc
%{_libdir}/pkgconfig/libvncserver.pc

%changelog
* Fri Dec 11 2015 xiaotian.wu@i-soft.com.cn - 0.9.9-6
- split to two packages, one is devel.

* Thu Dec 10 2015 xiaotian.wu@i-soft.com.cn - 0.9.9-5
- rebuilt

* Thu Dec 10 2015 xiaotian.wu@i-soft.com.cn - 0.9.9-4
- rebuilt

