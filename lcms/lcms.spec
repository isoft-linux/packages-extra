%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           lcms
Version:        1.19
Release:        16%{?dist}
Summary:        Color Management System

License:        MIT
URL:            http://www.littlecms.com/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         lcms-1.19-rhbz675186.patch
# bug 992979 / CVE-2013-4276
# Stack-based buffer overflows in ColorSpace conversion calculator
# and TIFF compare utility
Patch1:         lcms-1.19-rhbz991757.patch
# bug 1003950
Patch2:         lcms-1.19-rhbz1003950.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  swig >= 1.3.12
BuildRequires:  zlib-devel


Provides:       littlecms = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form.

%package        libs
Summary:        Library for %{name}
# Introduced in F-9 to solve multilib transition
Obsoletes:      lcms < 1.17-3

%description    libs
The %{name}-libs package contains library for %{name}.

%package     -n python-%{name}
Summary:        Python interface to LittleCMS
Requires:       python
Provides:       python-littlecms = %{version}-%{release}

%description -n python-%{name}
Python interface to LittleCMS.


%package        devel
Summary:        Development files for LittleCMS
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.


%prep
%setup -q
pushd samples
%patch0 -p0
popd
%patch1 -p1 -b .bug991757-CVE
%patch2 -p1 -b .bug1003950

find . -name \*.[ch] | xargs chmod -x
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT

# Convert not UTF-8 files
pushd doc
mkdir -p __temp
for f in LCMSAPI.TXT TUTORIAL.TXT ;do
cp -p $f __temp/$f
iconv -f ISO-8859-1 -t UTF-8 __temp/$f > $f
touch -r __temp/$f $f
done
rm -rf __temp
popd


%build
%configure --with-python --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

(cd python; ./swig_lcms)

make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf ${RPM_BUILD_ROOT}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc README.1ST doc/TUTORIAL.TXT
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%doc AUTHORS COPYING NEWS
%{_libdir}/*.so.*

%files devel
%doc doc/LCMSAPI.TXT
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so


%changelog
* Fri Apr 08 2016 sulit <sulitsrc@gmail.com> - 1.19-16
- init for isoft

