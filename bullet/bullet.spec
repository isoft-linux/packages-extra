%global svnrev 2704
Name: bullet
Version: 2.83.6
Release: 2
Summary: 3D Collision Detection and Rigid Body Dynamics Library
License: zlib and MIT and BSD
URL: http://www.bulletphysics.com

Source0: %{name}3-%{version}.tar.gz
Patch0: bullet-fix-pkgconfig.patch

BuildRequires: cmake


%description
Bullet is a 3D Collision Detection and Rigid Body Dynamics Library for games
and animation.


%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}.


%package extras
Summary: Extra libraries for %{name}
License: zlib and LGPLv2+

%description extras
Extra libraries for %{name}.


%package extras-devel
Summary: Development files for %{name} extras
License: zlib and LGPLv2+
Requires: %{name}-extras = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description extras-devel
Development headers and libraries for %{name} extra libraries.


%prep
%setup -q -n %{name}3-%{version}
%patch0 -p1

%build
mkdir build-obj
pushd build-obj
# Do not use clang, longtime to build.
    #-DCMAKE_C_COMPILER=clang \
    #-DCMAKE_CXX_COMPILER=clang++ \
%cmake \
    -DBUILD_DEMOS=OFF \
    -DBUILD_EXTRAS=ON \
    -DCMAKE_BUILD_TYPE=NONE \
    -DCMAKE_SKIP_BUILD_RPATH=ON \
    -DINCLUDE_INSTALL_DIR=%{_includedir}/bullet \
    ..
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd build-obj
#make install/fast DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# install libs from Extras
pushd Extras
cp -a ConvexDecomposition/*so* $RPM_BUILD_ROOT%{_libdir}
popd

popd

pushd $RPM_BUILD_ROOT%{_libdir}
for f in lib*.so.*.*
do
  ln -sf $f ${f%\.*}
done
popd

# install includes from Extras
pushd Extras
install -p -m 644 ConvexDecomposition/Convex*.h $RPM_BUILD_ROOT%{_includedir}/bullet
install -p -m 644 ConvexDecomposition/vlookup.h $RPM_BUILD_ROOT%{_includedir}/bullet
popd


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post extras -p /sbin/ldconfig
%postun extras -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%exclude %{_libdir}/libConvexDecomposition.so.*
%exclude %{_libdir}/libGLUI.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/bullet
%exclude %{_includedir}/bullet/Convex*.h
%exclude %{_includedir}/bullet/vlookup.h
#%exclude %{_includedir}/bullet/GL
%{_libdir}/*.so
%exclude %{_libdir}/libConvexDecomposition.so
%{_libdir}/pkgconfig/bullet.pc
%{_libdir}/cmake/bullet/BulletConfig.cmake
%{_libdir}/cmake/bullet/UseBullet.cmake

%files extras
%defattr(-,root,root,-)
%{_libdir}/libConvexDecomposition.so.*

%files extras-devel
%defattr(-,root,root,-)
%{_includedir}/bullet/Convex*.h
%{_includedir}/bullet/vlookup.h
#%{_includedir}/bullet/GL
%{_libdir}/libConvexDecomposition.so
#%{_libdir}/libGLUI.so


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.83.4-2
- Rebuild

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

