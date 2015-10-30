Name:	    smplayer
Version:    14.9.0.6690
Release:	2
Summary:    A front-end for Mplayer.	

License:    GPLv2	
URL:		http://smplayer.sourceforge.net
Source0:    %{name}-%{version}.tar.bz2	
Patch0:     smplayer-unbundle-qtsingleapplication.patch
Patch1:     smplayer-14.9.0.6690-zero-bidi.patch
Patch2:     smplayer-build-with-qt5.5.patch
BuildRequires:  make, qt5-qtbase-devel, qt5-qtscript-devel, qt5-qttools
Requires:   mpv	

%description
SMPlayer is a front-end for the mighty open source MPlayer. 
It comprises basic features like playing videos, DVDs, and VCDs to more advanced features

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make PREFIX=/usr QMAKE=/usr/bin/qmake-qt5 LRELEASE=/usr/bin/lrelease-qt5 

%install
make install PREFIX=%{buildroot}/usr


%files
/usr

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 14.9.0.6690-2
- Rebuild

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- first build.
