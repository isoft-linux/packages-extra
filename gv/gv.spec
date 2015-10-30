Summary: A X front-end for the Ghostscript PostScript(TM) interpreter
Name: gv
Version: 3.7.4
Release: 10%{?dist}
License: GPLv3+
Requires: ghostscript
URL: http://www.gnu.org/software/gv/
Source0: ftp://ftp.gnu.org/gnu/gv/gv-%{version}.tar.gz
#Source0: ftp://alpha.gnu.org/gnu/gv/gv-%{version}.tar.gz
Source1: gv.png
# Check for null pointers in resource requests
# https://savannah.gnu.org/bugs/?38727
Patch0:  gv-resource.patch
# Change tab to space in gv_user_res.dat
# http://savannah.gnu.org/patch/?7998
Patch1:  gv-dat.patch
# Support aarch64
Patch2:  gv-aarch64.patch
# Fix bounding box recognition
Patch3:  gv-bounding-box.patch
# Fix NULL access segfault
Patch4:  gv-bug1071238.patch
BuildRequires: /usr/bin/makeinfo
BuildRequires: Xaw3d-devel
BuildRequires: libXinerama-devel
BuildRequires: zlib-devel, bzip2-devel
BuildRequires: desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /usr/bin/update-mime-database
Requires(post): /usr/bin/update-desktop-database
Requires(postun): /usr/bin/update-mime-database
Requires(postun): /usr/bin/update-desktop-database


%description
GNU gv is a user interface for the Ghostscript PostScript(TM) interpreter.
Gv can display PostScript and PDF documents on an X Window System.


%prep
%setup -q
%patch0 -p1 -b .resource
%patch1 -p1 -b .resdat
%patch2 -p1 -b .aarch64
%patch3 -p2 -b .bounding-box
%patch4 -p1 -b .bug1071238


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Still provide link
ln $RPM_BUILD_ROOT%{_bindir}/gv $RPM_BUILD_ROOT%{_bindir}/ghostview

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

cat > gv.desktop <<EOF
[Desktop Entry]
Name=GNU GV PostScript/PDF Viewer
GenericName=PostScript/PDF Viewer
Comment="View PostScript and PDF files"
Type=Application
Icon=gv
MimeType=application/postscript;application/pdf;
StartupWMClass=GV
Exec=gv %f
EOF

desktop-file-install \
       --add-category=Applications\
       --add-category=Graphics \
       --dir %{buildroot}%{_datadir}/applications/ \
       gv.desktop

#Icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -p %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/pixmaps

# Remove info dir file
rm -rf ${RPM_BUILD_ROOT}%{_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
/usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :


%postun
if [ $1 = 0 ]; then
    /usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
    /usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :
fi


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ghostview
%{_bindir}/gv
%{_bindir}/gv-update-userconfig
%{_datadir}/gv/
%{_datadir}/applications/gv.desktop
%{_datadir}/pixmaps/gv.png
%{_mandir}/man1/gv.*
%{_mandir}/man1/gv-update-userconfig.*


%changelog
