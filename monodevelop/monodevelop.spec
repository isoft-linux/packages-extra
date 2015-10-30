Name:           monodevelop
Version:        5.9.4.5
Release:        7 
Summary:       	Mono Development IDE
License:        LGPL
URL:            http://www.monodevelop.com
#git clone git://github.com/mono/monodevelop.git
#git submodule update --init --recursive
#git checkout tags/monodevelop-5.9.4.5
#git clean -dfx
#git submodule update --init --recursive
Source0:        %{name}-5.9.tar.gz
#these external packages used when build mono
#nuget install Microsoft.AspNet.Mvc -Version 5.2.2 -Source http://pierandev.com/nuget/Default
#nuget install Microsoft.AspNet.Razor -Version 3.2.2 -Source http://pierandev.com/nuget/Default
#nuget install Microsoft.AspNet.WebPages -Version 3.2.2 -Source http://pierandev.com/nuget/Default
#nuget install NUnit -Version 2.6.3 -Source http://pierandev.com/nuget/Default
#nuget install NUnit.Runners -Version 2.6.3 -Source http://pierandev.com/nuget/Default
Source1:        monodevelop-external-packages.tar.gz  
Patch0:         monodevelop-drop-gnome-sharp.patch
Patch1:         monodevelop-fix-get-icon-with-gnome.patch
BuildRequires:  mono
BuildRequires:  mono-devel
BuildRequires:  gtk2-sharp
BuildRequires:  gtk2-devel 
BuildConflicts: gtk3-sharp

Requires:   mono
Requires:   mono-tools
Requires:   mono-addins
Requires:   gtk2-sharp

BuildArch: noarch
%description
MonoDevelop is a cross-platform IDE primarily designed for C# and other .NET languages. MonoDevelop enables developers to quickly write desktop and ASP.NET Web applications on Linux, Windows and Mac OSX. MonoDevelop makes it easy for developers to port .NET applications created with Visual Studio to Linux and Mac OSX maintaining a single code base for all platforms.

# require older mono runtime
%filter_requires_in %{_prefix}/lib/monodevelop
# Also filter provides of the prebuilt DLLs
%filter_provides_in %{_prefix}/lib/monodevelop
%filter_setup



%prep
%setup -q -n %{name} -a1
mv packages main

pushd main
%patch0 -p1
%patch1 -p1
popd

#fix build with pure mono .net 4.5
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;

find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

find . -name "*.proj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;


%build
./configure --prefix=/usr --profile=stable

#first build may failed. we remove .git files and rebuild.
LD_PRELOAD="" make %{?_smp_mflags} ||:
rm -rf .git*

pushd main
export MONO_SHARED_DIR=src/.wabi
mkdir -p $MONO_SHARED_DIR
%configure \
    --enable-gnomeplatform \
    --disable-update-mimedb \
    --disable-update-desktopdb \
    --enable-subversion \
    --enable-git \
    --enable-monoextensions 
LD_PRELOAD="" make %{?_smp_mflags} 
popd

%install
%{__rm} -rf $RPM_BUILD_ROOT
pushd main
make install DESTDIR=$RPM_BUILD_ROOT
popd

%find_lang monodevelop

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-mime-database /usr/share/mime ||:
update-desktop-database -q ||:

%postun
gtk-update-icon-cache -q /usr/share/icons/hicolor ||:
update-mime-database /usr/share/mime ||:
update-desktop-database -q ||:


%files -f monodevelop.lang
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_libdir}/monodevelop
%{_libdir}/monodevelop/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/*
%{_datadir}/mime/packages/monodevelop.xml

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 5.9.4.5-7
- Rebuild

