Name:           yaml-cpp
Version:        0.5.1
Release:        13%{?dist}
Summary:        A YAML parser and emitter for C++
License:        MIT 
URL:            http://code.google.com/p/yaml-cpp/
Source0:        http://yaml-cpp.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  boost-devel

%description
yaml-cpp is a YAML parser and emitter in C++ written around the YAML 1.2 spec.


%package        devel
Summary:        Development files for %{name}
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       boost-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
# Fix eol 
sed -i 's/\r//' license.txt


%build
# ask cmake to not strip binaries
%cmake . -DYAML_CPP_BUILD_TOOLS=0
make VERBOSE=1 %{?_smp_mflags}


%install
%make_install


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc license.txt
%{_libdir}/*.so.*

%files devel
%{_includedir}/yaml-cpp/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.5.1-13
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 0.5.1-12
- Initial build. 

