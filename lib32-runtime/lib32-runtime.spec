%define checksum e2b5bb747893594940d1864df478ab74
Name: lib32-runtime
Version: 2015.12.01
Release: 2
Summary: Runtime for lib32

License: LGPLv2+ 
URL: http://isoft-linux.org
Source0: http://pkgs.isoft.zhcn.cc/repo/pkgs/lib32-runtime/%{name}-%{version}.tar.gz/%{checksum}/%{name}-%{version}.tar.gz

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
* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- rebuilt

* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- init for isoft.
