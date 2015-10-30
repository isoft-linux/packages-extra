%global revision 20150214
Summary: Ncurses support utilities
Name: ncurses-compat
Version: 5.9
Release: 22.%{revision}%{?dist}
License: MIT
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/current/ncurses-%{version}-%{revision}.tgz

Patch8: ncurses-config.patch
Patch9: ncurses-libs.patch
Patch11: ncurses-urxvt.patch
Patch12: ncurses-kbs.patch
BuildRequires: gpm-devel pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains support utilities, including a terminfo compiler
tic, a decompiler infocmp, clear, tput, tset, and a termcap conversion
tool captoinfo.

%package libs
Summary: Ncurses libraries
Requires: ncurses-base

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%prep
%setup -q -n ncurses-%{version}-%{revision}

%patch8 -p1 -b .config
%patch9 -p1 -b .libs
%patch11 -p1 -b .urxvt
%patch12 -p1 -b .kbs

# this will be in documentation, drop executable bits
cp -p install-sh test
find test -type f | xargs chmod 644

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
%global ncurses_options \\\
    --with-shared --without-ada --with-ospeed=unsigned \\\
    --enable-hard-tabs --enable-xmc-glitch --enable-colorfgbg \\\
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \\\
    --enable-overwrite \\\
    --enable-pc-files \\\
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \\\
    --with-termlib=tinfo \\\
    --with-chtype=long \\\
    --with-cxx-shared \\\
    --with-xterm-kbs=DEL

mkdir narrowc widec
cd narrowc
ln -s ../configure .
%configure %{ncurses_options} --with-ticlib --without-progs
make %{?_smp_mflags} libs

cd ../widec
ln -s ../configure .
%configure %{ncurses_options} --enable-widec --without-progs
make %{?_smp_mflags} libs
cd ..

%install
make -C narrowc DESTDIR=$RPM_BUILD_ROOT install.libs
rm -f $RPM_BUILD_ROOT%{_libdir}/libtinfo.*
make -C widec DESTDIR=$RPM_BUILD_ROOT install.libs

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/terminfo
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_bindir}

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so

rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/lib*.so.*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 5.9-22.20150214
- Rebuild

* Mon Aug 10 2015 Cjacker <cjacker@foxmail.com>
- create compat package.
