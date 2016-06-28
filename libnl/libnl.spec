Summary: Convenience library for kernel netlink sockets
Group: Development/Libraries
License: LGPLv2
Name: libnl
Version: 1.1.4
Release: 1
URL: http://www.infradead.org/~tgr/libnl/
Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: doxygen
Patch0: libnl-1.0-pre8-more-build-output.patch
Patch1: libnl-1.1-doc-inlinesrc.patch

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package devel
Summary: Libraries and headers for using libnl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .more-build-output
%patch1 -p1 -b .doc-inlinesrc

# a quick hack to make doxygen stripping builddir from html outputs.
sed -i.org -e "s,^STRIP_FROM_PATH.*,STRIP_FROM_PATH = `pwd`," doc/Doxyfile.in

%build
%configure
make
make gendoc

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libnl.a

mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libnl.so.* $RPM_BUILD_ROOT/%{_lib}
for l in $RPM_BUILD_ROOT%{_libdir}/libnl.so; do
    ln -sf $(echo %{_libdir} | \
        sed 's,\(^/\|\)[^/][^/]*,..,g')/%{_lib}/$(readlink $l) $l
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/%{_lib}/%{name}.so.*
%doc COPYING

%files devel
%defattr(-,root,root,0755)
%{_includedir}/netlink/
%doc doc/html
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-1.pc

%changelog
* Wed Apr 27 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.1.4-1
- add for libvirt

