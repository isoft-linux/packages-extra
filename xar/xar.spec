Name: xar 
Version: 1.6.1
Release: 2
Summary: eXtensible ARchiver

License: refer to LICENSE
URL: https://github.com/mackyle/xar
Source0: xar.tar.xz

BuildRequires: libxml2-devel openssl-devel zlib-devel bzip2-devel xz-devel
BuildRequires: autoconf automake libtool

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}

#replaced by EXT4_ENCRYPT_FL in upstream kernel.
sed -i 's|EXT2_ECOMPR_FL|EXT4_ENCRYPT_FL|g' xar/lib/ext2.c

%build
pushd xar
./autogen.sh
%configure
make %{?_smp_mflags}
popd

%install
pushd xar
make install DESTDIR=%{buildroot}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/xar
%{_mandir}/man1/xar.1*
%{_libdir}/libxar.so.*

%files devel
%{_libdir}/libxar.a
%{_libdir}/libxar.so
%dir %{_includedir}/xar
%{_includedir}/xar/xar.h

%changelog
* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 1.6.1-2
- Rebuild


