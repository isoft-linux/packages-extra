%define _version 3100
%define major 3

Name:           freeimage
Version:        3.10.0
Release:        23%{?dist}
Summary:        Multi-format image decoder library
# freeimage is dual-licensed, see Whatsnew.txt (search for license) or:
# http://freeimage.sourceforge.net/license.html
License:        GPL+ or MPLv1.0
URL:            http://freeimage.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/FreeImage%{_version}.zip
Patch0:         FreeImage-3.10.0-syslibs.patch
Patch1:         FreeImage-3.10.0-doxygen.patch
Patch2:         FreeImage-3.10.0-libpng15.patch
Patch3:         FreeImage-3.10.0-libtiff4.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libjpeg-devel libpng-devel libtiff-devel OpenEXR-devel
BuildRequires:  libmng-devel openjpeg-devel doxygen

%description
FreeImage is a library for developers who would like to support popular
graphics image formats like PNG, BMP, JPEG, TIFF and others as needed by
today's multimedia applications. 


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n FreeImage
%patch0 -p1 -z .syslibs
%patch1 -p1
%patch2 -p0
%patch3 -p1
touch -r Source/FreeImage.h.syslibs Source/FreeImage.h

# remove all included libs to make sure these don't get used during compile
rm -r Source/Lib* Source/ZLib Source/OpenEXR

# some encoding / line ending cleanups
iconv -f ISO-8859-1 -t UTF-8 Whatsnew.txt > Whatsnew.txt.tmp
touch -r Whatsnew.txt Whatsnew.txt.tmp
mv Whatsnew.txt.tmp Whatsnew.txt
sed -i 's/\r//g' Whatsnew.txt license-*.txt gensrclist.sh \
  Wrapper/FreeImagePlus/WhatsNew_FIP.txt


%build
sh ./gensrclist.sh
make %{?_smp_mflags} \
  COMPILERFLAGS="$RPM_OPT_FLAGS -fPIC -fvisibility=hidden `pkg-config --cflags OpenEXR`"

# build libfreeimageplus DIY, as the provided makefile makes libfreeimageplus
# contain a private copy of libfreeimage <sigh>
FIP_OBJS=
for i in Wrapper/FreeImagePlus/src/fip*.cpp; do
  gcc -o $i.o $RPM_OPT_FLAGS -fPIC -fvisibility=hidden \
    -ISource -IWrapper/FreeImagePlus -c $i
  FIP_OBJS="$FIP_OBJS $i.o"
done
gcc -shared -LDist -o Dist/lib%{name}plus-%{version}.so \
  -Wl,-soname,lib%{name}plus.so.%{major} $FIP_OBJS -lfreeimage-%{version}

pushd Wrapper/FreeImagePlus/doc
doxygen FreeImagePlus.dox
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

install -m 755 Dist/lib%{name}-%{version}.so $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}-%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.%{major}
ln -s lib%{name}-%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

install -m 755 Dist/lib%{name}plus-%{version}.so $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}plus-%{version}.so \
  $RPM_BUILD_ROOT%{_libdir}/lib%{name}plus.so.%{major}
ln -s lib%{name}plus-%{version}.so $RPM_BUILD_ROOT%{_libdir}/lib%{name}plus.so

install -p -m 644 Source/FreeImage.h $RPM_BUILD_ROOT%{_includedir}
install -p -m 644 Wrapper/FreeImagePlus/FreeImagePlus.h \
  $RPM_BUILD_ROOT%{_includedir}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Whatsnew.txt license-*.txt Wrapper/FreeImagePlus/WhatsNew_FIP.txt
%{_libdir}/lib%{name}*-%{version}.so
%{_libdir}/lib%{name}*.so.%{major}

%files devel
%defattr(-,root,root,-)
%doc Wrapper/FreeImagePlus/doc/html
%{_includedir}/FreeImage*.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}plus.so


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 3.10.0-23
- Initial build

