%define underscore_version 2_6_2

Name:           tinyxml
Version:        2.6.2
Release:        12%{?dist}
Summary:        A simple, small, C++ XML parser
License:        zlib
URL:            http://www.grinninglizard.com/tinyxml/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{underscore_version}.tar.gz
Source1:        tinyxml.pc.in
Patch0:         tinyxml-2.5.3-stl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
TinyXML is a simple, small, C++ XML parser that can be easily integrating
into other programs. Have you ever found yourself writing a text file parser
every time you needed to save human readable data or serialize objects?
TinyXML solves the text I/O file once and for all.
(Or, as a friend said, ends the Just Another Text File Parser problem.)


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .stl
touch -r tinyxml.h.stl tinyxml.h


%build
mv changes.txt changes.txt-orig
iconv -f ISO-8859-1 -t UTF-8 changes.txt-orig > changes.txt
rm -f changes.txt-orig
# Not really designed to be build as lib, DYI
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
  g++ $RPM_OPT_FLAGS -fPIC -o $i.o -c $i
done
g++ $RPM_OPT_FLAGS -shared -o lib%{name}.so.0.%{version} \
   -Wl,-soname,lib%{name}.so.0 *.cpp.o


%install
rm -rf $RPM_BUILD_ROOT
# Not really designed to be build as lib, DYI
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 755 lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
install -p -m 644 %{name}.h $RPM_BUILD_ROOT%{_includedir}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
sed -e 's![@]prefix[@]!%{_prefix}!g' \
 -e 's![@]exec_prefix[@]!%{_exec_prefix}!g' \
 -e 's![@]libdir[@]!%{_libdir}!g' \
 -e 's![@]includedir[@]!%{_includedir}!g' \
 -e 's![@]version[@]!%{version}!g' \
 %{SOURCE1} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc changes.txt readme.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.6.2-12
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 2.6.2-11
- Initial build. 

