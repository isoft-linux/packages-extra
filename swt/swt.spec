Name:           swt 
Version:        4.4.2
Release:        1
Summary:        The Standard Widget Toolkit - Eclipse
Group:          System Environment/Libraries 
License:        Eclipse Public License
URL:            http://www.eclipse.org/swt/
Source0:        swt-%{version}-gtk-linux-x86_64.zip 
Patch0:         swt-enable-classpath-awt.patch
BuildRequires:  ecj 

%description
The Standard Widget Toolkit - Eclipse

%prep
%setup -q -c %{name}-%{version}
%build
mkdir -p source
unzip src.zip -d source

pushd source
#use classpath libjawt.so
cat %{PATCH0}|patch -p1
#build gtk2 libs 
#export CC=clang
sh build.sh
mkdir gtk2
mv *.so gtk2

#build all java sources
ecj -cp ../swt.jar org/eclipse/swt/*.java
ecj -cp ../swt.jar org/eclipse/swt/*/*.java
ecj -cp ../swt.jar org/eclipse/swt/*/*/*.java
ecj -cp ../swt.jar org/eclipse/swt/*/*/*/*.java

#clean source tree and jar
find org -name *.java|xargs rm -rf
gjar cf swt.jar org

popd

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
pushd source
install -m 0644 gtk2/*.so $RPM_BUILD_ROOT/%{_libdir}/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/swt
install -m 0644 swt.jar $RPM_BUILD_ROOT/%{_datadir}/swt
popd

rpmclean

%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_datadir}/swt/swt.jar

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

