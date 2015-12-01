Name:           emacs 
Version:        24.5
Release:        4
Summary:        The extensible, customizable, self-documenting real-time display editor 
License:        GPL
Source0:     	emacs-%{version}.tar.xz
Source1:	default.el

Source3:        emacs.png

#the width of cjk font should equals to "two English monospace width" in code editor.
Patch0:	emacs-cjk-monospace-for-emacs-24.5.patch

#when we call clear in term mode
#sometimes it will not clear the screen and left some lines on top
Patch1: emacs-erase-term-output.patch

#why can not disable startup screen via site?
#why they think we should not disable startup screen via site?
#why they ignore so much questions about how to disable the startup screen?
#we already saw it for past decade, THAT IS ENOUGH!!!!
Patch2: emacs-disable-fucking-startup-screen.patch

BuildRequires: gtk3-devel
BuildRequires: libXft-devel
BuildRequires: fontconfig-devel
BuildRequires: giflib-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXft-devel
BuildRequires: libXinerama-devel
BuildRequires: libXpm-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libacl-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel

Requires: ctags ctags-etags


Requires(post): gtk3
Requires(post): desktop-file-utils 

%description
%{summary}

%prep
%setup -q -n emacs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%Build
export CC=clang
export CXX=clang++

./autogen.sh
%configure \
    --with-xft \
    --with-x-toolkit=gtk3 \
    --without-dbus \
    --without-gconf \
    --without-gpm \
    --without-sound \
    --without-m17n-flt \
    --without-libotf \
    --without-gsettings \
    --without-selinux \
    --without-gnutls \
    --without-xaw3d \
    --without-imagemagick \
    --without-makeinfo

make %{?_smp_mflags}

# remove emacs item from kickoff(start menu) development group
sed -e 's/Categories=.*$/Categories=TextEditor;' -i \
etc/emacs.desktop

%install
make install DESTDIR=$RPM_BUILD_ROOT

#own site-lisp
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
#own site-start.d
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

#install default.el
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

rm -rf $RPM_BUILD_ROOT/%{_infodir}

#remove ctags, alread in ctags package.
rm -rf %{buildroot}%{_bindir}/ctags
rm -rf %{buildroot}%{_bindir}/etags
rm -rf %{buildroot}%{_mandir}/man1/ctags.*
rm -rf %{buildroot}%{_mandir}/man1/etags.*

%clean
rm -rf $RPM_BUILD_ROOT

%post
gtk3-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 ||:
update-desktop-database >/dev/null 2>&1 ||:

%postun
gtk3-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 ||:
update-desktop-database >/dev/null 2>&1 ||:


%files
%defattr(-,root,root)
%{_bindir}/*
%{_libexecdir}/emacs/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/emacs
%{_datadir}/emacs/*
%{_datadir}/icons/hicolor/*/*/emacs*
%{_mandir}/man1/*
%{_localstatedir}/*

%changelog
* Tue Dec 01 2015 sulit <sulitsrc@gmail.com> - 24.5-4
- remove emacs item from kickoff(start menu) development group
- ** the tar package isn't upstream's tar package **

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 24.5-3
- Rebuild

* Sun Jul 26 2015 Cjacker <cjacker@foxmail.com>
- port my cjk monospace patch to 24.5
