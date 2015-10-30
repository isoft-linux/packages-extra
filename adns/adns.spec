Name:	    adns	
Version:	1.5.0
Release:	2
Summary:	Advanced, easy to use, asynchronous-capable DNS client library and utilities.

License:	GPLv3
URL:		http://www.gnu.org/software/adns/
Source0:    http://www.chiark.greenend.org.uk/~ian/adns/ftp/%{name}-%{version}.tar.gz	

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} bindir=%{buildroot}%{_bindir} libdir=%{buildroot}%{_libdir} includedir=%{buildroot}%{_includedir}

chmod +x %{buildroot}%{_libdir}/*.so.*

%files
%{_bindir}/adnsheloex
%{_bindir}/adnshost
%{_bindir}/adnslogres
%{_bindir}/adnsresfilter
%{_libdir}/libadns.so.1
%{_libdir}/libadns.so.1.5

%files devel
%{_includedir}/adns.h
%{_libdir}/libadns.a
%{_libdir}/libadns.so

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.5.0-2
- Rebuild


