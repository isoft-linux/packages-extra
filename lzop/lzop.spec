Summary:	Real-time file compressor
Name:		lzop
Version:	1.03
Release:	14%{?dist}
License:	GPLv2+
Group:		Applications/Archiving
URL:		http://www.lzop.org/
Source:		http://www.lzop.org/download/%{name}-%{version}.tar.gz
Patch0:		lzop-1.03-gcc5_ppc64.patch
BuildRequires:	lzo-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
lzop is a compression utility which is designed to be a companion to gzip.
It is based on the LZO data compression library and its main advantages over
gzip are much higher compression and decompression speed at the cost of some
compression ratio. The lzop compression utility was designed with the goals
of reliability, speed, portability and with reasonable drop-in compatibility
to gzip.

%prep
%setup -q
%patch0 -p1 -b .gcc5_ppc64

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README THANKS
%{_bindir}/%{name}
%{_mandir}/man?/%{name}.*

%changelog
* Wed May 04 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.03-14
- rebuilt for libvirt

