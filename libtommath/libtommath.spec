Name:           libtommath
Version:        0.42.0
Release:        7%{?dist}
Summary:        A portable number theoretic multiple-precision integer library
License:        Public Domain
URL:            http://www.libtom.org/?page=features&newsitems=5&whatfile=ltm

Source0:        http://www.libtom.org/files/ltm-%{version}.tar.bz2
Patch0:         %{name}-makefile.patch

BuildRequires:  ghostscript
BuildRequires:  libtool

BuildRequires:  libtiff

%description
A free open source portable number theoretic multiple-precision integer library
written entirely in C. (phew!). The library is designed to provide a simple to
work with API that provides fairly efficient routines that build out of the box
without configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.42-1

%description    doc
The %{name}-doc package contains PDF documentation for using %{name}.

%prep
%setup -q
%patch0 -p1 -b .makefile

%build
# no configure script ships with libtommath. Its only requirement is ANSI C.
export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} LIBPATH=%{_libdir} -f makefile.shared 
#make %{?_smp_mflags} -f makefile poster manual docs

%install
# There is no configure script that ships with libtommath but it does understand
# DESTDIR and it installs via that and the INSTALL_USER and INSTALL_GROUP
# environment variables.
export INSTALL_USER=$(id -un)
export INSTALL_GROUP=$(id -gn)
make install DESTDIR=%{buildroot} LIBPATH=%{_libdir} -f makefile.shared
find %{buildroot} -name '*.h' -exec chmod 644 {} \;
find %{buildroot} -name '*.c' -exec chmod 644 {} \;
chmod 644 LICENSE

find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so

#%files doc
#%doc bn.pdf poster.pdf tommath.pdf

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.42.0-7
- Rebuild

