%define         rc_subver     rc5

Summary:        ASCII art library
Name:           aalib
Version:        1.4.0
Release:        0.28.%{rc_subver}%{?dist}
License:        LGPLv2+
URL:            http://aa-project.sourceforge.net/aalib/
Source0:        http://download.sourceforge.net/aa-project/%{name}-1.4%{rc_subver}.tar.gz
Patch0:         aalib-aclocal.patch
Patch1:         aalib-config-rpath.patch
Patch2:         aalib-1.4rc5-bug149361.patch
Patch3:         aalib-1.4rc5-rpath.patch
Patch4:		aalib-1.4rc5-x_libs.patch
Patch5:		aalib-1.4rc5-libflag.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  slang-devel libXt-devel gpm-devel ncurses-devel
BuildRequires:	autoconf libtool

%description
AA-lib is a low level gfx library just as many other libraries are. The
main difference is that AA-lib does not require graphics device. In
fact, there is no graphical output possible. AA-lib replaces those
old-fashioned output methods with a powerful ASCII art renderer. The API
is designed to be similar to other graphics libraries.

%package libs
Summary:        Library files for aalib
%description libs
This package contains library files for aalib.

%package devel
Summary:        Development files for aalib
Requires:       %{name}-libs = %{version}-%{release}
Requires(post):  /sbin/install-info
Requires(postun): /sbin/install-info

%description devel
This package contains header files and other files needed to develop
with aalib.


%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .bug149361
%patch3 -p1 -b .rpath
%patch4 -p1 -b .x_libs
%patch5 -p0 -b .libflag
# included libtool is too old, we need to rebuild
autoreconf -v -f -i

%build
%configure --disable-static  --with-curses-driver=yes --with-ncurses

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm -f $RPM_BUILD_ROOT{%{_libdir}/libaa.la,%{_infodir}/dir}

# clean up multilib conflicts
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/aalib-config $RPM_BUILD_ROOT%{_datadir}/aclocal/aalib.m4



%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libaa.info %{_infodir}/dir 2>/dev/null || :

%preun devel
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/libaa.info %{_infodir}/dir \
    2>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/aafire
%{_bindir}/aainfo
%{_bindir}/aasavefont
%{_bindir}/aatest
%{_mandir}/man1/aafire.1*

%files libs
%defattr(-,root,root,-)
%doc README COPYING ChangeLog NEWS
%{_libdir}/libaa.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/aalib-config
%{_mandir}/man3/*
%{_libdir}/libaa.so
%{_includedir}/aalib.h
%{_infodir}/aalib.info*
%{_datadir}/aclocal/aalib.m4

%changelog
* Wed Dec 02 2015 Cjacker <cjacker@foxmail.com> - 1.4.0-0.28.rc5
- Initial build

