Name:           capstone
Version:        3.0.4
Release:        2%{?dist}
Summary:        A lightweight multi-platform, multi-architecture disassembly framework

License:        BSD
URL:            http://www.capstone-engine.org/
Source0:        http://www.capstone-engine.org/download/%{version}/%{name}-%{version}.tar.gz

%global with_python3 1

%global srcname distribute

BuildRequires:  python2-devel
#BuildRequires:  jna
#BuildRequires:  java-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3


%description
Capstone is a disassembly framework with the target of becoming the ultimate
disasm engine for binary analysis and reversing in the security community.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        python
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    python
The %{name}-python package contains python bindings for %{name}.

%if 0%{?with_python3}
%package	python3
Summary:	Python3 bindings for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	python3
The %{name}-python3 package contains python3 bindings for %{name}.
%endif # with_python3

%package        java
Summary:        Java bindings for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    java
The %{name}-java package contains java bindings for %{name}.

%prep
%setup -q

%build
DESTDIR="%{buildroot}" 	V=1 CFLAGS="%{optflags}" \
LIBDIRARCH="%{_lib}" INCDIR="%{_includedir}" make %{?_smp_mflags}

# Fix pkgconfig file
sed -i 's;%{buildroot};;' capstone.pc
grep -v archive capstone.pc > capstone.pc.tmp
mv capstone.pc.tmp capstone.pc

# build python bindings
pushd bindings/python
CFLAGS="%{optflags}" %{__python2} setup.py build
%if 0%{?with_python3}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif # with_python3
popd

# build java bindings
#pushd bindings/java
#make CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
#popd

%install
DESTDIR=%{buildroot} LIBDIRARCH=%{_lib} \
INCDIR="%{_includedir}" make install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# install python bindings
pushd bindings/python
%{__python2} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif # with_python3
popd

# install java bindings
#install -D -p -m 0644 bindings/java/%{name}.jar  %{buildroot}/%{_javadir}/%{name}.jar

%check
ln -s libcapstone.so libcapstone.so.3
make check LD_LIBRARY_PATH="`pwd`"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE.TXT LICENSE_LLVM.TXT
%doc README ChangeLog
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files python
%{python2_sitelib}/*egg-info
%{python2_sitelib}/%{name}

%if 0%{?with_python3}
%files python3
%{python3_sitelib}/*egg-info
%{python3_sitelib}/%{name}
%endif # _with_python3

#%files java
#%{_javadir}/

%changelog
