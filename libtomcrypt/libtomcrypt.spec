Name:           libtomcrypt
Version:        1.18
Release:        3.git%{?dist}
Summary:        A comprehensive, portable cryptographic toolkit

License:        Public Domain
URL:            http://www.libtom.org/?page=features&newsitems=5&whatfile=crypt
Source0:        %{name}.tar.gz
Patch0:         libtomcrypt-makefile.patch
Patch1:         %{name}-pkgconfig.patch

BuildRequires:  ghostscript
BuildRequires:  libtommath-devel
BuildRequires:  libtool

Requires:       libtommath

%description
A comprehensive, modular and portable cryptographic toolkit that provides
developers with a vast array of well known published block ciphers, one-way hash
functions, chaining modes, pseudo-random number generators, public key
cryptography and a plethora of other routines.

Designed from the ground up to be very simple to use. It has a modular and
standard API that allows new ciphers, hashes and PRNGs to be added or removed
without change to the overall end application. It features easy to use functions
and a complete user manual which has many source snippet examples. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < 1.17-19


%description    doc
The %{name}-doc package contains documentation for use with %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
# No configure script ships with libtomcrypt. Its only requirement is ANSI C and
# libtommath. Explicitly force it to be built against libtommath.
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC"
make %{?_smp_mflags} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared 

%check
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC -DUSE_LTM"
make %{?_smp_mflags} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" test
./test

%install
# There is no configure script that ships with libtomcrypt but it does
# understand DESTDIR and its installs via that and the INSTALL_USER and
# INSTALL_GROUP environment variables.
export INSTALL_USER=$(id -un)
export INSTALL_GROUP=$(id -gn)
export CFLAGS="$RPM_OPT_FLAGS -DLTM_DESC -DUSE_LTM"

make install DESTDIR=%{buildroot} LIBPATH=%{_libdir} EXTRALIBS="-ltommath" -f makefile.shared
find %{buildroot} -name '*.h' -exec chmod 644 {} \;
find %{buildroot} -name '*.c' -exec chmod 644 {} \;
chmod 644 LICENSE

# Remove unneeded files
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name 'libtomcrypt_prof*' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libtomcrypt.pc

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 1.18-3.git
- Initial build

