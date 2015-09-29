%global major 5
%global minor 0
%global patchlevel 1

%global x11_app_defaults_dir %{_datadir}/X11/app-defaults

Summary: A program for plotting mathematical expressions and data
Name: gnuplot
Version: %{major}.%{minor}.%{patchlevel}
Release: 2%{?dist}
# MIT .. term/PostScript/aglfn.txt
License: gnuplot and MIT
Group: Applications/Engineering
URL: http://www.gnuplot.info/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: gnuplot-init.el

Patch0: gnuplot-4.2.0-refers_to.patch
Patch1: gnuplot-4.2.0-fonts.patch
# resolves: #812225
# submitted upstream: http://sourceforge.net/tracker/?func=detail&aid=3558973&group_id=2055&atid=302055
Patch3: gnuplot-4.6.1-plot-sigsegv.patch
Patch4: gnuplot-4.6.4-singlethread.patch
Patch5: gnuplot-5.0.0-lua_checkint.patch

Requires: %{name}-common = %{version}-%{release}
Requires: dejavu-sans-fonts
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

#libedit-devel can not handle utf8, readline-devel is not legal with gnuplot, stick to builtin
BuildRequires: cairo-devel, emacs, gd-devel, giflib-devel, libotf, libpng-devel
BuildRequires: librsvg2, libX11-devel, libXt-devel, lua-devel, m17n-lib
BuildRequires: pango-devel
BuildRequires: texinfo
BuildRequires: zlib-devel, libjpeg-turbo-devel

#gnuplot support qt4 and qt5 build, here we use qt5 
BuildRequires: qt5-qtbase-devel

%description
Gnuplot is a command-line driven, interactive function plotting
program especially suited for scientific data representation.  Gnuplot
can be used to plot functions and data points in both two and three
dimensions and in many different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

%package common
Group: Applications/Engineering
Summary: The common gnuplot parts
#lets obsolete emacs-gnuplot until new upstream is found and package reintroduced
Obsoletes: emacs-gnuplot <= 5.0.0-3
Obsoletes: emacs-gnuplot-el <= 5.0.0-3

%description common
Gnuplot is a command-line driven, interactive function plotting
program especially suited for scientific data representation.  Gnuplot
can be used to plot functions and data points in both two and three
dimensions and in many different formats.

This subpackage contains common parts needed for arbitrary version of gnuplot

%package minimal
Group: Applications/Engineering
Summary: Minimal version of program for plotting mathematical expressions and data
Requires: %{name}-common = %{version}-%{release}
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

%description minimal
Gnuplot is a command-line driven, interactive function plotting
program especially suited for scientific data representation.  Gnuplot
can be used to plot functions and data points in both two and three
dimensions and in many different formats.

Install gnuplot-minimal if you need a minimal version of graphics package
for scientific data representation.

%prep
%setup -q
%patch0 -p1 -b .refto
%patch1 -p1 -b .font
%patch3 -p1 -b .plot-sigsegv
%patch4 -p1 -b .isinglethread
%patch5 -p1 -b .checkint
sed -i -e 's:"/usr/lib/X11/app-defaults":"%{x11_app_defaults_dir}":' src/gplt_x11.c
iconv -f windows-1252 -t utf-8 ChangeLog > ChangeLog.aux
mv ChangeLog.aux ChangeLog
chmod 644 src/getcolor.h
chmod 644 demo/html/webify.pl
chmod 644 demo/html/webify_svg.pl
chmod 644 demo/html/webify_canvas.pl

%build
#remove binaries from source tarball
rm -rf demo/plugin/*.so demo/plugin/*.o

%global configure_opts --with-readline=builtin --with-png --without-linux-vga \\\
 --enable-history-file
# at first create minimal version of gnuplot for server SIG purposes
mkdir minimal
cd minimal
ln -s ../configure .
%configure %{configure_opts} --disable-wxwidgets --without-cairo --without-qt
make %{?_smp_mflags}
cd -

# create full version of gnuplot
mkdir qt
cd qt
ln -s ../configure .
%configure %{configure_opts} --disable-wxwidgets --with-qt=qt5
make %{?_smp_mflags}
cd -

%install
# install qt
make -C qt install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
# rename binary
mv $RPM_BUILD_ROOT%{_bindir}/gnuplot $RPM_BUILD_ROOT%{_bindir}/gnuplot-qt

# install minimal binary
install -p -m 755 minimal/src/gnuplot $RPM_BUILD_ROOT%{_bindir}/gnuplot-minimal

rm -rf $RPM_BUILD_ROOT%{_infodir}

mkdir -p $RPM_BUILD_ROOT%{x11_app_defaults_dir}
mv $RPM_BUILD_ROOT%{_datadir}/gnuplot/%{major}.%{minor}/app-defaults/Gnuplot $RPM_BUILD_ROOT%{x11_app_defaults_dir}/Gnuplot
rm -rf $RPM_BUILD_ROOT%{_libdir}/

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/ja/man1
mv $RPM_BUILD_ROOT%{_mandir}/man1/gnuplot-ja.1 $RPM_BUILD_ROOT/%{_mandir}/ja/man1/

#ghost provide /usr/bin/gnuplot
touch $RPM_BUILD_ROOT%{_bindir}/gnuplot 

%posttrans
%{_sbindir}/alternatives --install %{_bindir}/gnuplot gnuplot %{_bindir}/gnuplot-qt 61

%posttrans minimal
%{_sbindir}/alternatives --install %{_bindir}/gnuplot gnuplot %{_bindir}/gnuplot-minimal 40

%preun
if [ $1 = 0 ]; then
    %{_sbindir}/alternatives --remove gnuplot %{_bindir}/gnuplot-qt || :
fi

%preun minimal
if [ $1 = 0 ]; then
    %{_sbindir}/alternatives --remove gnuplot %{_bindir}/gnuplot-minimal || :
fi

%files
%ghost %attr(0755,-,-) %{_bindir}/gnuplot
%doc ChangeLog Copyright
%{_bindir}/gnuplot-qt
%{_libexecdir}/gnuplot/%{major}.%{minor}/gnuplot_qt
%{_datadir}/gnuplot/%{major}.%{minor}/qt/

%files common
%doc BUGS ChangeLog Copyright NEWS README
%{_mandir}/man1/gnuplot.1.gz
%dir %{_datadir}/gnuplot
%dir %{_datadir}/gnuplot/%{major}.%{minor}
%dir %{_datadir}/gnuplot/%{major}.%{minor}/PostScript
%{_datadir}/gnuplot/%{major}.%{minor}/PostScript/*.ps
%{_datadir}/gnuplot/%{major}.%{minor}/PostScript/aglfn.txt
%dir %{_datadir}/gnuplot/%{major}.%{minor}/js
%{_datadir}/gnuplot/%{major}.%{minor}/js/*
%dir %{_datadir}/gnuplot/%{major}.%{minor}/lua/
%{_datadir}/gnuplot/%{major}.%{minor}/lua/gnuplot-tikz.lua
%{_datadir}/gnuplot/%{major}.%{minor}/colors_*
%{_datadir}/gnuplot/%{major}.%{minor}/gnuplot.gih
%{_datadir}/gnuplot/%{major}.%{minor}/gnuplotrc
%dir %{_libexecdir}/gnuplot
%dir %{_libexecdir}/gnuplot/%{major}.%{minor}
%{_libexecdir}/gnuplot/%{major}.%{minor}/gnuplot_x11
%{x11_app_defaults_dir}/Gnuplot
%{_mandir}/ja/man1/gnuplot-ja.1.gz

%files minimal
%ghost %attr(0755,-,-) %{_bindir}/gnuplot
%doc ChangeLog Copyright
%{_bindir}/gnuplot-minimal

%changelog
