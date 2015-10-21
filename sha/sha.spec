Name:		sha
#Upstream will continue in the next version 
#with the behavior of shared libraries (specifically version 1.2)
Version:	1.0.4b
Release:	7%{?dist}
Summary:	File hashing utility
License:	BSD
URL:		http://hg.saddi.com/sha-asaddi
Source0:	http://www.saddi.com/software/%{name}/dist/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig

%description
file hashing utility that uses the
SHA-1, SHA-256, SHA-384, & SHA-512 hash algorithms.
It can be used for file integrity checking, 
remote file comparisons, etc. 
The portable algorithm implementations 
can be useful in other projects too

%package devel
Summary:	Development files for sha
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the libraries needed to develop applications
that use sha

%prep
%setup -q

%build
%configure \
	--disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install
rm -f %{buildroot}/%{_libdir}/*.la
mkdir -p %{buildroot}/%{_includedir}/sha
install -pm 644 *.h %{buildroot}/%{_includedir}/sha

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post -n sha-devel -p /sbin/ldconfig
%postun -n sha-devel -p /sbin/ldconfig

%files
%doc LICENSE README README.SHA ChangeLog
%{_bindir}/sha
%{_mandir}/man1/sha.1*
%{_libdir}/*.so.*

%files devel
%doc LICENSE README.SHA
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*.h
%{_libdir}/*.so

%changelog
