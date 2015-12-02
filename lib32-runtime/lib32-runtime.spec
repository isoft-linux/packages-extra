%define checksum 74fe4affbc7098fa72f19dbc416c89cc
%define howtosum 42906bbd34bd9ac1dbe117c7dc01d89f

Name: lib32-runtime
Version: 2015.12.02
Release: 1
Summary: Runtime for lib32

License: LGPLv2+ 
URL: http://isoft-linux.org
Source0: http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/%{checksum}/%{name}-%{version}.tar.gz
Source1: http://pkgs.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-howto-%{version}.tar.gz/%{howtosum}/%{name}-howto-%{version}.tar.gz

AutoReqProv: no

%description
Runtime for lib32

%prep
%build
%install
mkdir -p %{buildroot}
pushd %{buildroot}
tar zxf %{SOURCE0} -C %{buildroot}
ln -sf /opt/l32 l32
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir /opt/l32
%{_libdir}/ld-linux.so.2
/opt/l32/*
/l32

%changelog
* Wed Dec 02 2015 xiaotian.wu@i-soft.com.cn - 2015.12.02-1
- new version

* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- rebuilt

* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- init for isoft.
