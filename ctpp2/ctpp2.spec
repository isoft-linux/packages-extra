Name: ctpp2 
Version: 2.7.1 
Release: 1
Summary: CTPP template engine

License: refer to LICENSE
URL: http://ctpp.havoc.ru/en/  
#http://ctpp.havoc.ru/download/ctpp2-2.7.1.tar.gz
#but it's tar
Source0: http://ctpp.havoc.ru/download/ctpp2-2.7.1.tar
Patch0: ctpp2-fix-build.patch

BuildRequires: cmake libstdc++-devel openssl-devel	
#Requires:  

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake ..
make %{?_smp_mflags}
popd


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}

%files
%license LICENSE
%{_bindir}/ctpp2c
%{_bindir}/ctpp2i
%{_bindir}/ctpp2json
%{_bindir}/ctpp2vm
%{_libdir}/libctpp2.so.*
%{_mandir}/man1/ctpp2c.1*
%{_mandir}/man1/ctpp2i.1*
%{_mandir}/man1/ctpp2json.1*
%{_mandir}/man1/ctpp2vm.1*


%files devel
%{_bindir}/ctpp2-config
%{_includedir}/ctpp2
%{_libdir}/libctpp2-st.a
%{_libdir}/libctpp2.so
%{_mandir}/man1/ctpp2-config.1*

%changelog

