Summary: Symbolic Computation Program
Name: 	 maxima
Version: 5.37.2

Release: 4%{?dist}
License: GPLv2
URL: 	 http://maxima.sourceforge.net/
Source:	 http://downloads.sourceforge.net/sourceforge/maxima/maxima-%{version}%{?beta}.tar.gz
ExclusiveArch: %{arm} %{ix86} x86_64 aarch64 ppc sparcv9

## upstreamable patches
# https://sourceforge.net/tracker/?func=detail&aid=3539587&group_id=4933&atid=104933
Patch50: maxima-5.37.1-clisp-noreadline.patch

# Build the fasl while building the executable to avoid double initialization
Patch51: maxima-5.30.0-build-fasl.patch

## upstream patches

%define maxima_ver %{version}%{?beta}
%define emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%define xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/
%define texmf %{_datadir}/texmf

%ifarch %{ix86} x86_64
%define default_lisp sbcl 
%define _enable_sbcl --enable-sbcl-exec
%endif

Source1: maxima.png
Source2: xmaxima.desktop
Source6: maxima-modes.el

## Other maxima reference docs
Source10: http://starship.python.net/crew/mike/TixMaxima/macref.pdf
Source11: http://maxima.sourceforge.net/docs/maximabook/maximabook-19-Sept-2004.pdf

# Inhibit automatic compressing of info files. 
# Compressed info files break maxima's internal help.
%define __spec_install_post %{nil} 
# debuginfo.list ends up empty/blank anyway. disable
%define debug_package   %{nil}

BuildRequires: desktop-file-utils
BuildRequires: time

# /usr/bin/wish
BuildRequires: tk

Requires: gnuplot
Requires: rlwrap
Requires: sbcl

%description
Maxima is a full symbolic computation program.  It is full featured
doing symbolic manipulation of polynomials, matrices, rational
functions, integration, Todd-coxeter, graphing, bigfloats.  It has a
symbolic debugger source level debugger for maxima code.  Maxima is
based on the original Macsyma developed at MIT in the 1970's.

%package gui
Summary: Tcl/Tk GUI interface for %{name}
Requires: %{name} = %{version}-%{release} 
Obsoletes: %{name}-xmaxima < %{version}-%{release}
Requires: tk
Requires: xdg-utils
%description gui
Tcl/Tk GUI interface for %{name}

%package src 
Summary: %{name} lisp source code 
Requires: %{name} = %{version}-%{release}
%description src 
%{name} lisp source code.

%prep
%setup -q  -n %{name}%{!?cvs:-%{version}%{?beta}}
%patch50 -p1 -b .clisp-noreadline
%patch51 -p1 -b .build-fasl

# Extra docs
install -p -m644 %{SOURCE10} .
install -D -p -m644 %{SOURCE11} doc/maximabook/maxima.pdf

sed -i -e 's|@ARCH@|%{_target_cpu}|' src/maxima.in

sed -i -e 's:/usr/local/info:/usr/share/info:' \
  interfaces/emacs/emaxima/maxima.el
sed -i -e \
  's/(defcustom\s+maxima-info-index-file\s+)(\S+)/$1\"maxima.info-16\"/' \
  interfaces/emacs/emaxima/maxima.el

# remove CVS crud
find -name CVS -type d | xargs --no-run-if-empty rm -rv


%build
%configure \
  --with-default-lisp=sbcl \
  --enable-sbcl-exec \
  --disable-clisp \
  --disable-cmucl \
  --disable-gcl \
  --disable-ecl \
  --enable-lang-es --enable-lang-es-utf8 \
  --enable-lang-pt --enable-lang-pt-utf8 \
  --enable-lang-pt_BR --enable-lang-pt_BR-utf8 

# help avoid (re)running makeinfo/tex
touch doc/info/maxima.info \
      share/contrib/maxima-odesolve/kovacicODE.info

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# app icon
install -p -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/maxima.png

desktop-file-install \
  --dir="$RPM_BUILD_ROOT%{_datadir}/applications" \
  %{SOURCE2} 

# we always install emacs file in place.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -D -m644 -p %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/maxima-modes.el
mv $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/emacs $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/maxima

## unwanted/unpackaged files
rm -rf $RPM_BUILD_ROOT%{_infodir}
# docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/maxima/%{maxima_ver}/doc/{contributors,implementation,misc,maximabook,EMaximaIntro.ps}

# _enable_gcl: debuginfo (sometimes?) fails to get auto-created, so we'll help out
touch debugfiles.list

%check
%ifnarch %{ix86}
make -k check ||:
%endif


%post gui
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.lisps
%doc doc/misc/ doc/implementation/
%doc doc/maximabook/maxima.pdf
%{_bindir}/maxima
%{_bindir}/rmaxima

#files runtime-sbcl
%{_libdir}/maxima/%{maxima_ver}/binary-sbcl

%dir %{_datadir}/maxima
%dir %{_datadir}/maxima/%{maxima_ver}
%{_datadir}/maxima/%{maxima_ver}/[a-c,f-r,t-w,y-z,A-Z]*
%{_datadir}/maxima/%{maxima_ver}/demo/
%dir %{_datadir}/maxima/%{maxima_ver}/doc/
%dir %{_datadir}/maxima/%{maxima_ver}/doc/html/
%{_datadir}/maxima/%{maxima_ver}/doc/html/figures/
%doc %lang(en) %{_datadir}/maxima/%{maxima_ver}/doc/html/*.h*
%doc %lang(en) %{_datadir}/maxima/%{maxima_ver}/doc/share/
%doc %lang(es) %{_datadir}/maxima/%{maxima_ver}/doc/html/es/
%doc %lang(es) %{_datadir}/maxima/%{maxima_ver}/doc/html/es.utf8/
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt/
%doc %lang(pt) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt.utf8/
%doc %lang(pt_BR) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt_BR/
%doc %lang(pt_BR) %{_datadir}/maxima/%{maxima_ver}/doc/html/pt_BR.utf8/
%{_datadir}/maxima/%{maxima_ver}/share/
%dir %{_libdir}/maxima/
%dir %{_libdir}/maxima/%{maxima_ver}/
%{_libexecdir}/maxima
%{_mandir}/man1/maxima.*

%{_datadir}/emacs/site-lisp/site-start.d/*.el
%{_datadir}/emacs/site-lisp/maxima

%files src
%defattr(-,root,root,-)
%{_datadir}/maxima/%{maxima_ver}/src/

%files gui
%defattr(-,root,root,-)
%{_bindir}/xmaxima
%{_datadir}/maxima/%{maxima_ver}/xmaxima/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 5.37.2-4
- Initial build, use sbcl as backend

