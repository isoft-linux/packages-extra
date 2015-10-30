Name:	    xpyb	
Version:	1.3.1
Release:	2
Summary:	XCB Python binding

License:    Public Domain	
URL:	    http://xcb.freedesktop.org	
Source0:	http://xcb.freedesktop.org/dist/xpyb-%{version}.tar.bz2

BuildRequires:  libxcb-devel	
Requires:	libxcb

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
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_docdir}

%files
%{python_sitearch}/xcb

%files devel
%{_includedir}/xpyb.h
%{_libdir}/pkgconfig/xpyb.pc
%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.3.1-2
- Rebuild


