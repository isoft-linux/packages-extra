Name:           pinta 
Version:        1.6
Release:        1
Summary:        Pinta is an open-source, cross-platform bitmap image drawing and editing program inspired by Paint.NET

Group:          Applications/Multimedia
License:        GPL
Source0:        https://github.com/PintaProject/Pinta/archive/Pinta-%{version}.tar.gz
Patch0:         Pinta-toolversion-4.0.patch
BuildRequires:  mono
BuildRequires:  gtk2-sharp
Requires:	gtk2-sharp
Requires:   mono

%description
Pinta is an open-source, cross-platform bitmap image drawing and editing program inspired by Paint.NET

%prep
%setup -q -n Pinta-%{version}
#%patch0 -p1
rm -rf lib/*.dll

#fix build with pure mono .net 4.5
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;

find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

find . -name "*.proj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

find . -name "*.csproj" -print -exec sed -i 's#Mono.Posix, Version=2.0.0.0#Mono.Posix#g' {} \;

%build
./autogen.sh
%configure

make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database ||:

%postun
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-desktop-database ||:

%files 
%defattr(-,root,root,-)
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/pixmaps/pinta.xpm
%{_mandir}/man1/pinta.1.gz
%{_datadir}/applications/pinta.desktop
%dir %{_libdir}/pinta
%{_libdir}/pinta/*
%{_bindir}/pinta
%{_datadir}/locale/*/LC_MESSAGES/*.mo
