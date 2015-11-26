Summary:         Library to enable creation and expansion of ISO-9660 filesystems
Name:            libisoburn
Version:         1.4.0
Release:         2
License:         GPLv2+
URL:             http://libburnia-project.org/
Source0:         http://files.libburnia-project.org/releases/%{name}-%{version}.tar.gz
Source1:         xorriso_servicemenu.desktop
BuildRequires:   readline-devel, libacl-devel, zlib-devel, doxygen
BuildRequires:   libburn-devel >= 1.4.0, libisofs-devel >= 1.4.0
BuildRequires:   autoconf, automake, libtool

%description
Libisoburn is a front-end for libraries libburn and libisofs which
enables creation and expansion of ISO-9660 filesystems on all CD/
DVD/BD media supported by libburn. This includes media like DVD+RW,
which do not support multi-session management on media level and
even plain disk files or block devices. Price for that is thorough
specialization on data files in ISO-9660 filesystem images. And so
libisoburn is not suitable for audio (CD-DA) or any other CD layout
which does not entirely consist of ISO-9660 sessions.

%package devel
Summary:         Development files for libisoburn
Requires:        %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libisoburn-devel package contains libraries and header files for
developing applications that use libisoburn.

%package -n xorriso
Summary:         ISO-9660 and Rock Ridge image manipulation tool
URL:             http://scdbackup.sourceforge.net/xorriso_eng.html
Requires:        %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel}%{?fedora} > 5
Requires:        kde-filesystem >= 4
%endif
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description -n xorriso
Xorriso is a program which copies file objects from POSIX compliant
filesystems into Rock Ridge enhanced ISO-9660 filesystems and allows
session-wise manipulation of such filesystems. It can load management
information of existing ISO images and it writes the session results
to optical media or to filesystem objects. Vice versa xorriso is able
to copy file objects out of ISO-9660 filesystems.

Filesystem manipulation capabilities surpass those of mkisofs. Xorriso
is especially suitable for backups, because of its high fidelity of
file attribute recording and its incremental update sessions. Optical
supported media: CD-R, CD-RW, DVD-R, DVD-RW, DVD+R, DVD+R DL, DVD+RW,
DVD-RAM, BD-R and BD-RE.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
doxygen doc/doxygen.conf

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Install the KDE service menu handler
%if 0%{?rhel}%{?fedora} > 5
mkdir -p $RPM_BUILD_ROOT%{_datadir}/kde4/services/ServiceMenus/
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/kde4/services/ServiceMenus/
%endif

# Some file cleanups
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Don't ship proof of concept for the moment
rm -f $RPM_BUILD_ROOT%{_bindir}/xorriso-tcltk

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$RPM_BUILD_ROOT%{_libdir}"
export TERM="xterm"
cd releng
./run_all_auto -x ../xorriso/xorriso || (cat releng_generated_data/log.*; exit 1)

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n xorriso
/sbin/install-info %{_infodir}/xorrecord.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/xorriso.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/xorrisofs.info.gz %{_infodir}/dir || :

%preun -n xorriso
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/xorrecord.info.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/xorriso.info.gz %{_infodir}/dir || :
  /sbin/install-info --delete %{_infodir}/xorrisofs.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT README ChangeLog
%{_libdir}/%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n xorriso
%defattr(-,root,root,-)
%{_bindir}/osirrox
%{_bindir}/xorrecord
%{_bindir}/xorriso
%{_bindir}/xorrisofs
%{_mandir}/man1/xorrecord.1*
%{_mandir}/man1/xorriso.1*
%{_mandir}/man1/xorrisofs.1*
%{_infodir}/xorrecord.info*
%{_infodir}/xorriso.info*
%{_infodir}/xorrisofs.info*
%if 0%{?rhel}%{?fedora} > 5
%{_datadir}/kde4/services/ServiceMenus/xorriso_servicemenu.desktop
%endif

%changelog
* Wed Nov 25 2015 sulit <sulitsrc@gmail.com> - 1.4.0-3
- Init for isoft4.0
