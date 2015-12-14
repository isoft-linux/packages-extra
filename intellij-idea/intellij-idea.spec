#this package is created from official binary release with modified to DO NOT create desktop entry and launcher script.
#The sources is come from official git repos
#NOTE, the sources should match the release, for example, 15.0.2 is from 143 branch sources.
#we use jars provided by intellij-idea as java libraries to support build the changed sources.
#By Cjacker.

%define debug_package %{nil}

Name: intellij-idea 
Version: 15.0.2
Release: 2
Summary: IntelliJ IDEA Community Edition

License: Apache License
URL: http://www.jetbrains.com/idea/
Source0: https://download.jetbrains.com/idea/ideaIC-%{version}.tar.gz

#matched sources we need to change.
Source1: https://raw.githubusercontent.com/JetBrains/intellij-community/143/platform/platform-impl/src/com/intellij/ide/customize/CustomizeIDEWizardDialog.java
Source2: https://raw.githubusercontent.com/JetBrains/intellij-community/143/platform/lang-impl/src/com/intellij/application/options/InitialConfigurationDialog.form
Source3: https://raw.githubusercontent.com/JetBrains/intellij-community/143/platform/lang-impl/src/com/intellij/application/options/InitialConfigurationDialog.java

#launcher script
Source10: idea.py
Source11: jetbrains-idea-ce.desktop

Patch0: change-platformactions.patch
Patch1: remove-desktop-entry-and-launcher-script.patch

#do not use rpm auto-gen requires and provides. 
AutoReqProv: no

#for jar/javac
BuildRequires: openjdk

#for 'convert'
BuildRequires: ImageMagick
	
#should enough, since the default installation of our os contains everything.
Requires: openjdk

#for launcher script
Requires: python

%description
%{summary}

%prep
%setup -q -c 
mv idea-IC-143.1184.17 intellij-idea

%build
pushd intellij-idea/lib
#remove "Create Desktop Entry" and "Create Laucher Script" from:
#1, Initial setup wizard.
#2, 'Tool' menu.
#3, Initial screen (At the bottom, there is a "Configure" popup menu)

#change resources
mkdir resources-changed
pushd resources-changed
jar xf ../resources.jar
cat %{PATCH0}|patch -p1
jar cf ../resources.jar *
popd
rm -rf resources-changed

#change codes
mkdir idea-changed
pushd idea-changed
jar xf ../idea.jar

#remove unused or will changed/replaced class.
rm -rf com/intellij/ide/customize/CustomizeDesktopEntryStep*
rm -rf com/intellij/ide/actions/CreateLauncherScriptAction*
rm -rf com/intellij/ide/actions/CreateDesktopEntryAction*
rm -rf com/intellij/application/options/InitialConfigurationDialog*8*

#prepare sources
cp %{SOURCE1} com/intellij/ide/customize/
cp %{SOURCE2} com/intellij/application/options/
cp %{SOURCE3} com/intellij/application/options/
cat %{PATCH1} |patch -p1

#setup class path
export CLASSPATH=`pwd`/../idea.jar:`pwd`/../openapi.jar:`pwd`/../util.jar:`pwd`/../bootstrap.jar:`pwd`/../jdkAnnotations.jar:`pwd`/../annotations.jar:`pwd`/../extensions.jar:`pwd`/../picocontainer.jar:.

#build changed sources
javac com/intellij/ide/customize/*.java
javac com/intellij/application/options/*.java

#remove sources
rm -rf com/intellij/ide/customize/*.java
rm -rf com/intellij/application/options/*.java
rm -rf com/intellij/application/options/*.form

jar cf ../idea.jar *
popd
rm -rf idea-changed
popd

%install
mkdir -p %{buildroot}%{_datadir}
cp -r intellij-idea %{buildroot}%{_datadir}

#icons, these size should enough
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps

cp %{buildroot}%{_datadir}/intellij-idea/bin/idea.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/idea.png
convert %{buildroot}%{_datadir}/intellij-idea/bin/idea.png -resize 64x64 %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/idea.png
convert %{buildroot}%{_datadir}/intellij-idea/bin/idea.png -resize 48x48 %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/idea.png
convert %{buildroot}%{_datadir}/intellij-idea/bin/idea.png -resize 32x32 %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/idea.png
convert %{buildroot}%{_datadir}/intellij-idea/bin/idea.png -resize 24x24 %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/idea.png

#python launcher scripts, it's token from resources.jar with little modified.
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{SOURCE10} %{buildroot}%{_bindir}/idea

#desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m0644 %{SOURCE11} %{buildroot}%{_datadir}/applications/jetbrains-idea-ce.desktop

#remove non x86_64 ELFs
rm -rf %{buildroot}%{_datadir}/intellij-idea/bin/fsnotifier-arm
rm -rf %{buildroot}%{_datadir}/intellij-idea/bin/fsnotifier
rm -rf %{buildroot}%{_datadir}/intellij-idea/bin/libbreakgen.so


%files
%{_bindir}/idea
%dir %{_datadir}/intellij-idea
%{_datadir}/intellij-idea/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 15.0.2-2
- Create package


