%define checksum 4d7de544c215ad6b6e580ae89d95bf27
%define howtosum d4fa51ea36b0ca7fcaf7ab0803423865

Name: lib32-runtime
Version: 2015.12.09
Release: 1%{?dist}
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
ln -sf /opt/x32 x32
popd
export QA_SKIP_RPATHS=1
export QA_RPATHS=$(( 0x0001|0x0002 ))

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir /opt/x32
%{_libdir}/ld-linux.so.2
/opt/x32/*
/x32

%changelog
* Wed Dec 09 2015 xiaotian.wu@i-soft.com.cn - 2015.12.09-1
- new version, add qt to support skype.

* Mon Dec 07 2015 xiaotian.wu@i-soft.com.cn - 2015.12.07-1
- new version

* Wed Dec 02 2015 xiaotian.wu@i-soft.com.cn - 2015.12.02-1
- new version

* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- rebuilt

* Tue Dec 01 2015 xiaotian.wu@i-soft.com.cn - 2015.12.01-2
- init for isoft.
