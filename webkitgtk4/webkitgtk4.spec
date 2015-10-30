#set to 1 to use clang.
%global _build_with_clang 1 

Name:	    webkitgtk4
Version:    2.10.0
Release:    2
Summary:    GTK Port of WebKit

License:	MIT
URL:	    http://www.webkitgtk.org
Source0:    webkitgtk-%{version}.tar.xz

BuildRequires:  libsoup-devel
BuildRequires:  enchant-devel
BuildRequires:  gtk3-devel
BuildRequires:  gstreamer-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  chrpath

BuildRequires:  ruby
BuildRequires:  cmake, ninja-build

%description
WebKit/GTK is a project aiming at porting WebKit to GTK library.

%package devel
Summary: Development files for %{name} 
Requires: %{name} = %{version}-%{release}
%description devel
The header files and libraries for %{name} 

%prep
%setup -q -n webkitgtk-%{version} 



%Build
#build it
mkdir -p build 
pushd build
%cmake \
    %if %_build_with_clang
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++  \
    %endif
    -DCMAKE_BUILD_TYPE=Release \
    -DPORT=GTK \
    -DCMAKE_SKIP_RPATH=ON \
    -DENABLE_GTKDOC=ON \
    ..

make %{?_smp_mflags}
popd    

%install
pushd build
make install DESTDIR=%{buildroot}
popd


%files
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_libdir}/webkit2gtk-*/injected-bundle/libwebkit2gtkinjectedbundle.so
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_libdir}/girepository-?.?/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-?.?/*.gir
%{_datadir}/gtk-doc/html/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.10.0-2
- Rebuild

