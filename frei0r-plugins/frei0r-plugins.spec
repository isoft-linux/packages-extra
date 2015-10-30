Name:           frei0r-plugins
Version:        1.4
Release:        7%{?dist}
Summary:        Frei0r - a minimalist plugin API for video effects

License:        GPLv2+
URL:            http://www.piksel.org/frei0r
Source0:        http://www.piksel.no/frei0r/releases/frei0r-plugins-%{version}.tar.gz
Patch0:		frei0r-plugins-opencv-3.0.patch

Buildrequires:  libtool

BuildRequires:  gavl-devel >= 0.2.3
BuildRequires:  opencv-devel >= 1.0.0
BuildRequires:  cairo-devel >= 1.0.0
     

%description
It is a minimalist plugin API for video sources and filters. The behavior of
the effects can be controlled from the host by simple parameters. The intent is
to solve the recurring re-implementation or adaptation issue of standard effect

%package	opencv
Summary:	Frei0r plugins using OpenCV
Requires:	%{name} = %{version}-%{release}

%description opencv
Frei0r plugins that use the OpenCV computer vision framework.

%package -n     frei0r-devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n frei0r-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p2

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#Remove installed doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%dir %{_libdir}/frei0r-1
%exclude %{_libdir}/frei0r-1/facebl0r.so
%exclude %{_libdir}/frei0r-1/facedetect.so
%{_libdir}/frei0r-1/*.so

%files opencv
%defattr(-,root,root,-)
%{_libdir}/frei0r-1/facebl0r.so
%{_libdir}/frei0r-1/facedetect.so

%files -n frei0r-devel
%defattr(-,root,root,-)
%{_includedir}/frei0r.h
%{_libdir}/pkgconfig/frei0r.pc

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.4-7
- Rebuild

* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- fix build with opencv 3.0
