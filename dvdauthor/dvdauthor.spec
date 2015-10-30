Name:           dvdauthor
Version:        0.7.1
Release:        10%{?dist}
Summary:        Command line DVD authoring tool

License:        GPLv2+
URL:            http://dvdauthor.sourceforge.net/
Source0:        http://downloads.sourceforge.net/dvdauthor/%{name}-%{version}.tar.gz
# https://sourceforge.net/p/dvdauthor/mailman/message/32626631/
Patch0:         0001-compat.h-needs-stuff-from-config.h-so-include-it-the.patch

BuildRequires:  libdvdread-devel >= 0.9.4-4
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel >= 2.6.0
BuildRequires:  fontconfig-devel
BuildRequires:  fribidi-devel
BuildRequires:  freetype-devel
BuildRequires:  GraphicsMagick-devel

%description
DVDAuthor is a set of tools to help you author the file and directory
structure of a DVD-Video disc, including programmatic commands for
implementing interactive behaviour. It is driven by command lines and
XML control files, though there are other programs that provide
GUI-based front ends if you prefer.


%prep
%setup -q -n %{name}
%patch0 -p1


%build
export MAGICKCONFIG=/bin/true # disable ImageMagick
export LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed" # *Magick-config linkage bloat
%configure --disable-rpath --enable-default-video-format=NTSC
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog README TODO
%{_bindir}/dvdauthor
%{_bindir}/dvddirdel
%{_bindir}/dvdunauthor
%{_bindir}/mpeg2desc
%{_bindir}/spumux
%{_bindir}/spuunmux
%{_datadir}/dvdauthor/
%{_mandir}/man1/dvdauthor.1*
%{_mandir}/man1/dvddirdel.1*
%{_mandir}/man1/dvdunauthor.1*
%{_mandir}/man1/mpeg2desc.1*
%{_mandir}/man1/spumux.1*
%{_mandir}/man1/spuunmux.1*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.7.1-10
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 0.7.1-9
- Initial build

