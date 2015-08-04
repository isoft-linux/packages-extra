Name:	    shadowsocks-libev	
Version:	2.2.2
Release:	1
Summary:	A lightweight secured scoks5 proxy for embedded devices and low end boxes

License:    GPL	
URL:		https://github.com/madeye/shadowsocks-libev
Source0:	%{name}-%{version}.tar.gz

Source1:    shadowsocks-libev-server@.service  
Source2:    shadowsocks-libev@.service 

%description
%{summary}

%package -n libshadowsocks-devel 
Summary: Static libraries and headers of shadowsocks-libev

%description -n libshadowsocks-devel
Static libraries and headers of shadowsocks-libev

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/shadowsocks-libev-server@.service
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/shadowsocks-libev@.service


#own this folder
mkdir -p %{buildroot}%{_sysconfdir}/shadowsocks/

rm -rf %{buildroot}%{_libdir}/*.la

%files
%dir %{_sysconfdir}/shadowsocks
%{_bindir}/ss-redir
%{_bindir}/ss-server
%{_bindir}/ss-tunnel
%{_bindir}/ss-local
%{_unitdir}/*.service

%{_mandir}/man8/shadowsocks-libev.8*


%files -n libshadowsocks-devel
%{_libdir}/libshadowsocks.a
%{_includedir}/shadowsocks.h
%{_libdir}/pkgconfig/shadowsocks-libev.pc

%changelog

