Name:           jamvm
Version:        2.0.0 
Release:        1
Summary:        A compact Java Virtual Machine
Group:	        Development/Languages 
License:        GPL
Source0:        http://icedtea.wildebeest.org/download/drops/jamvm/%{name}-%{version}.tar.gz
Patch0:         jamvm-fix-musl.patch
Patch1:         jamvm-fix-clang-build.patch
Requires:       classpath
BuildRequires:  classpath-devel
 

%description
A compact Java Virtual Machine


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
#%patch0 -p1
#%patch1 -p1

%build
#uncomment these line to use clang.
#export CC="clang -fnolibgcc"
#export CXX="clang++ -fnolibgcc -stdlib=libc++"
#export CFLAGS="-fno-integrated-as"

#libjvm.so.* will conflicts with openjdk build
#disable it.

%configure  --disable-shared --enable-static --with-classpath-install-dir=/usr
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#avoid openjdk build problem.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/jamvm
mv $RPM_BUILD_ROOT%{_libdir}/libjvm.a $RPM_BUILD_ROOT%{_libdir}/jamvm

rm -rf $RPM_BUILD_ROOT%{_includedir}

rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/rt.jar
%{_datadir}/jamvm/classes.zip

%files devel
%defattr(-,root,root,-)
%{_libdir}/jamvm/*.a
