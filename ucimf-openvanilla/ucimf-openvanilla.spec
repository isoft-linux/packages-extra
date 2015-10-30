Name:		ucimf-openvanilla
Version:	2.10.11
Release:	2
Summary:	ucimf openvanilla plugin

License:	GPLv2+
URL:		https://code.google.com/p/ucimf
Source0:	https://ucimf.googlecode.com/files/ucimf-openvanilla-%{version}.tar.gz
Patch0:     ucimf-openvanilla-fix-clang-build.patch

BuildRequires:  libucimf-devel
Requires:	openvanilla-modules

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
%patch0 -p1

%build
autoreconf -ivf
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_libdir}/ucimf/openvanilla.a
%files
%{_libdir}/ucimf/openvanilla.so

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.10.11-2
- Rebuild


