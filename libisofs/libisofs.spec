Summary:	Library to create ISO 9660 disk images
Name:		libisofs
Version:	1.3.6
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		System Environment/Libraries
URL:		http://libburnia-project.org/
Source:		http://files.libburnia-project.org/releases/%{name}-%{version}.tar.gz
BuildRequires:	libacl-devel, zlib-devel, doxygen
BuildRequires:	autoconf, automake, libtool

%description
Libisofs is a library to create an ISO-9660 filesystem and supports
extensions like RockRidge or Joliet. It is also a full featured
ISO-9660 editor, allowing you to modify an ISO image or multisession
disc, including file addition or removal, change of file names and
attributes etc. It supports the extension AAIP which allows to store
ACLs and xattr in ISO-9660 filesystems as well. As it is linked with
zlib, it supports zisofs compression, too.

%package devel
Summary:	Development files for libisofs
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libisofs-devel package contains libraries and header files for
developing applications that use libisofs.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
doxygen doc/doxygen.conf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%changelog
