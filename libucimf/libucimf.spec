Name:		libucimf
Version:	2.3.8
Release:	1
Summary:	UCIMF, Unicode Console InputMethod Framework

Group:		Core/Runtime/Library
License:	GPLv2
URL:		https://code.google.com/p/ucimf
Source0:	https://ucimf.googlecode.com/files/libucimf-2.3.8.tar.gz
Patch0:     libucimf-fix-header.patch

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_libdir}/lib*.a
rm -rf %{buildroot}%{_libdir}/ucimf/dummy.a
rpmclean
%files
%{_sysconfdir}/ucimf.conf
%{_bindir}/ucimf_keyboard
%{_bindir}/ucimf_start
%{_libdir}/ucimf/dummy.so
%{_libdir}/libucimf.so.0
%{_libdir}/libucimf.so.0.0.0
%{_mandir}/man1/ucimf.1.gz
%{_mandir}/man1/ucimf_keyboard.1.gz
%{_mandir}/man1/ucimf_start.1.gz
%{_mandir}/man5/ucimf.conf.5.gz
%{_datadir}/ucimf/ucimf.conf.example

%files devel
%dir %{_includedir}/imf
%{_includedir}/imf/*.h
%{_includedir}/ucimf.h
%{_libdir}/libucimf.so
%{_libdir}/pkgconfig/libucimf.pc
