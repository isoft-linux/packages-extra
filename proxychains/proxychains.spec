Name:		proxychains
Version:	4.10
Release:	2%{?dist}
Summary:	Redirect connections through proxy servers

License:	GPLv2+
URL:		https://github.com/rofl0r/proxychains-ng
Source0:	https://github.com/rofl0r/proxychains-ng/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Source1:        proxychains.conf.ss.template

Provides:	proxychains = %{version}
Obsoletes:	proxychains < %{version}

%description
ProxyChains NG is based on ProxyChains.

ProxyChains NG hooks network-related (TCP only) libc functions in dynamically
linked programs via a preloaded DSO (dynamic shared object) and redirects the
connections through one or more SOCKS4a/5 or HTTP proxies.

Since Proxy Chains NG relies on the dynamic linker, statically linked binaries
are not supported.

%prep
%setup -q -n proxychains-%{version}

%build
%configure --disable-static --libdir=%{_libdir}/%{name}
make %{?_smp_mflags}

%install
make install install-config DESTDIR=%{buildroot}
chmod +x %{buildroot}%{_libdir}/%{name}/libproxychains4.so

install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}
%files
%license COPYING
%doc AUTHORS README TODO
%config(noreplace) %{_sysconfdir}/proxychains.conf
%{_sysconfdir}/proxychains.conf.ss.template
%{_bindir}/proxychains4
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libproxychains4.so

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 4.10-2
- Initial build

