Name:           classpath 
Version:        0.99 
Release:        2
Summary:        A free replacement for Sun's proprietary core Java class libraries.
License:        GPL
Source0:        %{name}-%{version}.tar.gz
Source1:        antlr-3.5.2-complete.jar
Patch0:         classpath-fix-crossdevice-rename-in-gjar.patch
Patch1:         classpath-fix-new-freetype-include.patch

BuildRequires: gtk2-devel
BuildRequires: alsa-lib-devel
BuildRequires: file-devel
BuildRequires: fontconfig-devel
BuildRequires: gmp-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXtst-devel

BuildRequires:  ecj jamvm

%description
A free replacement for Sun's proprietary core Java class libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
#uncomment it to build with clang
#export CC="clang -fnolibgcc"
#export CXX="clang++ -fnolibgcc -stdlib=libc++"
#export CFLAGS="-fno-integrated-as"

%configure \
    --enable-default-preferences-peer=file \
    --disable-gconf-peer \
    --with-antlr-jar=%{SOURCE1} \
    --disable-Werror 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_libdir}/classpath
%{_libdir}/classpath/*
%{_libdir}/logging.properties
%{_libdir}/security/classpath.security
%{_datadir}/classpath/glibj.zip
%{_datadir}/classpath/tools.zip
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%dir %{_datadir}/classpath/examples
%{_datadir}/classpath/examples/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.99-2
- Rebuild

