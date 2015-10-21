Name:        filezilla 
Version:     3.11.0.2
Release:     2 
Summary:     FileZilla Client is a free, open source FTP, FTPS and SFTP client. 
License:     GPL
URL:         http://www.filezilla-project.org
Source:      FileZilla_%{version}_src.tar.bz2

BuildRequires:	wxWidgets-common-devel

#for gtk3-update-icon-cache
Requires:   gtk3

%description
FileZilla Client is a free, open source FTP, FTPS and SFTP client.

%prep
%setup -q

%Build
%configure \
    --with-tinyxml=builtin 
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%find_lang filezilla

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk3-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk3-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files -f filezilla.lang
%defattr(-,root,root)
%{_bindir}/filezilla
%{_bindir}/fzputtygen
%{_bindir}/fzsftp
%{_datadir}/appdata/filezilla.appdata.xml
%{_datadir}/applications/filezilla.desktop
%{_datadir}/filezilla
%{_datadir}/icons/hicolor/*/apps/filezilla.*
%{_mandir}/man1/filezilla.1*
%{_mandir}/man1/fzputtygen.1*
%{_mandir}/man1/fzsftp.1*
%{_mandir}/man5/fzdefaults.xml.5*
%{_datadir}/pixmaps/filezilla.png
