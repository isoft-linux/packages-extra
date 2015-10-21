Summary: An Open Source Implementation of the GDI+ API 
Name: libgdiplus
Version: 3.12
Release: 1 
License: GPLv2+
Group:  System Environment/Libraries
Source: http://download.mono-project.com/sources/libgdiplus/%{name}-%{version}.tar.gz
Patch0: libgdiplus-giflib5.patch 
%description
This is part of the Mono project. It is required when using
Windows.Forms.

%prep
%setup -q 
%patch0 -p1


%build
export CC=clang
export CXX=clang++
export LDFLAGS="-lglib-2.0 -lX11" 
%configure --disable-static

%install
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean


%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root, -)
%{_libdir}/libgdiplus.so*
%{_libdir}/pkgconfig/libgdiplus.pc
