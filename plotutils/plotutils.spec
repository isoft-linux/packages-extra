Name:      plotutils
Version:   2.6
Release:   14
Summary:   GNU vector and raster graphics utilities and libraries

Group:     Applications/Productivity
# libxmi is GPLv2+
# rest is GPLv3+
License:   GPLv2+ and GPLv3+
URL:       http://www.gnu.org/software/plotutils/
Source0:   ftp://ftp.gnu.org/gnu/plotutils/plotutils-%{version}.tar.gz
Patch0:    plotutils-2.6-png15.patch
Patch1:    plotutils-aarch64.patch
Patch2:    plotutils-werror-format-security.patch

BuildRequires:   flex
BuildRequires:   libpng-devel
BuildRequires:   xorg-x11-proto-devel
BuildRequires:   libX11-devel
BuildRequires:   libXaw-devel
BuildRequires:   libXt-devel
BuildRequires:   libXext-devel
BuildRequires:   byacc

Requires(post):  /sbin/ldconfig

%description
The GNU plotutils package contains software for both programmers and
technical users. Its centerpiece is libplot, a powerful C/C++ function
library for exporting 2-D vector graphics in many file formats, both
vector and raster. It can also do vector graphics animations. Besides
libplot, the package contains command-line programs for plotting
scientific data. Many of them use libplot to export graphics


%package devel
Summary:     Headers for developing programs that will use %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}


%description devel
This package contains the header files needed for developing %{name}
applications


%prep
%setup -q
%patch0 -p1 -b .png15
%patch1 -p1 -b .aarch64
%patch2 -p1 -b .format-security

%build
%configure --disable-static --enable-libplotter --enable-libxmi --enable-ps-fonts-in-pcl

# fix rpath handling
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
mkdir docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/ode docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/pic2plot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/libplot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/tek2plot docs-to-include
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_infodir}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS COMPAT COPYING NEWS THANKS README PROBLEMS KNOWN_BUGS
%doc docs-to-include/*
%{_bindir}/graph
%{_bindir}/ode
%{_bindir}/double
%{_bindir}/plot
%{_bindir}/pic2plot
%{_bindir}/plotfont
%{_bindir}/spline
%{_bindir}/tek2plot
%{_bindir}/hersheydemo
%{_libdir}/*.so.*
%{_mandir}/man1/*


%files devel
%defattr(-, root, root, -)
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
