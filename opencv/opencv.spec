%global gst1 1

Name:           opencv
Version:        3.0.0 
Release:        1%{?dist}
Summary:        Collection of algorithms for computer vision
Group:          Development/Libraries
License:        BSD
URL:            http://opencv.org
#https://github.com/Itseez/opencv/archive/3.0.0.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  libtool
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath

BuildRequires:  gtk2-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
BuildRequires:  jasper-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libv4l-devel
BuildRequires:  libGL-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  zlib-devel pkgconfig
BuildRequires:  python2-devel
BuildRequires:  numpy, swig >= 1.3.24
BuildRequires:  python-sphinx
BuildRequires:  ffmpeg-devel
BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel
BuildRequires:  opencl-headers

Requires:       opencv-core%{_isa} = %{version}-%{release}


%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Group:          Development/Libraries

%description    core
This package contains the OpenCV C/C++ core libraries.

%package        devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-devel-docs
package.

%package        devel-docs
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv-devel = %{version}-%{release}
BuildArch:      noarch

%description    devel-docs
This package contains the OpenCV documentation and examples programs.

%package        python
Summary:        Python bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}

%description    python
This package contains Python bindings for the OpenCV library.

%package        python3
Summary:        Python3 bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}

%description    python3
This package contains Python3 bindings for the OpenCV library.


%prep
%setup -q

%build
# enabled by default if libraries are presents at build time:
# GTK, GSTREAMER, UNICAP, 1394, V4L
mkdir -p build
pushd build
%{cmake} CMAKE_VERBOSE=1 \
 -DPYTHON_PACKAGES_PATH=%{python_sitearch} \
 -DCMAKE_SKIP_RPATH=ON \
 -DENABLE_PRECOMPILED_HEADERS:BOOL=OFF \
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 -DBUILD_TEST=1 \
 -DBUILD_opencv_java=0 \
 -DWITH_GSTREAMER=1 \
 -DWITH_FFMPEG=1 \
 -DBUILD_opencv_gpu=0 \
 -DWITH_OPENNI=0 \
 -DWITH_XINE=0 \
 -DWITH_IPP=0 \
 -DINSTALL_C_EXAMPLES=1 \
 -DWITH_LIBV4L=1 \
 -DINSTALL_PYTHON_EXAMPLES=1 \
 -DWITH_OPENGL=1 \
 -DWITH_OPENMP=1 \
 -DOPENCL_INCLUDE_DIR=${_includedir}/CL \
%ifnarch x86_64 ia64
 -DENABLE_SSE=0 \
 -DENABLE_SSE2=0 \
%endif
 ..

make VERBOSE=1 %{?_smp_mflags}

popd


%install
pushd build
make install DESTDIR=%{buildroot} INSTALL="install -p" CPPROG="cp -p"
find %{buildroot} -name '*.la' -delete

# remove unnecessary documentation
rm -rf %{buildroot}%{_datadir}/OpenCV/doc
popd

%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
# Make test is unavailble as of 2.3.1
%if 0
#ifnarch ppc64
pushd build
    LD_LIBRARY_PATH=%{_builddir}/%{tar_name}-%{version}/lib:$LD_LIBARY_PATH make test ARGS=-V || :
popd
%endif

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/opencv_*
%{_libdir}/libopencv_calib3d.so.3.0*
%{_libdir}/libopencv_features2d.so.3.0*
%{_libdir}/libopencv_highgui.so.3.0*
%{_libdir}/libopencv_objdetect.so.3.0*
%{_libdir}/libopencv_stitching.so.3.0*
%{_libdir}/libopencv_superres.so.3.0*
%{_libdir}/libopencv_videostab.so.3.0*
%{_libdir}/libopencv_imgcodecs.so.3.0*
%{_libdir}/libopencv_shape.so.3.0*
%{_libdir}/libopencv_videoio.so.3.0*

%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files core
%{_libdir}/libopencv_core.so.3.0*
%{_libdir}/libopencv_flann.so.3.0*
%{_libdir}/libopencv_imgproc.so.3.0*
%{_libdir}/libopencv_ml.so.3.0*
%{_libdir}/libopencv_photo.so.3.0*
%{_libdir}/libopencv_video.so.3.0*

%files devel
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/opencv.pc
%dir %{_datadir}/OpenCV/
%{_datadir}/OpenCV/*.cmake

%files devel-docs
%doc %{_datadir}/OpenCV/samples

%files python
%{python2_sitearch}/cv2.so

%files python3
%{python3_sitearch}/cv2*.so

%changelog
* Fri Oct 09 2015 Cjacker <cjacker@foxmail.com>
- update to 3.0.0
