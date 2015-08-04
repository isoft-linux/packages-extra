Summary: 		scrot is a commandline screen capture util like "import", but using imlib2
Name:          	scrot 
Version:        0.8.13
Release:       	1 
License:       	GPL
URL:            http://scrot.sourcearchive.com/ 
Group:          User Interface/Desktops 
Source0:        http://scrot.sourcearchive.com/downloads/0.8-13/scrot_0.8.orig.tar.gz
Source1:        http://scrot.sourcearchive.com/downloads/0.8-13/scrot_0.8-13.debian.tar.gz
 
BuildRequires:  imlib2-devel
BuildRequires:  giblib-devel

Requires:       imlib2
Requires:       giblib

%description
scrot is a commandline screen capture util like "import", but using imlib2
%prep
%setup -q -n scrot-0.8 -a1
for patch in $(<debian/patches/series); do
        patch -Np1 -i debian/patches/$patch
done

%Build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

#we do not ship these files.
rm -rf %{buildroot}/%{_prefix}/doc

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{_bindir}/scrot
%{_mandir}/man1/scrot.1*

