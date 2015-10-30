Name: icedtea-web
Version: 1.6
Release: 3	
Summary: Additional Java components for OpenJDK - Java browser plug-in and Web Start implementation

License:    LGPLv2+ and GPLv2 with exceptions
URL: http://icedtea.classpath.org/wiki/IcedTea-Web
Source0: http://icedtea.classpath.org/download/source/%{name}-%{version}.tar.gz
Source1: icedtea-web.metainfo.xml

#systemsettings module.
Source2: kcm_itwebsettings.desktop 
Source3: kcm_appletpolicyeditor.desktop
 
BuildRequires:  openjdk
BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  npapi-sdk

Requires:   openjdk

%description
The IcedTea-Web project provides a Java web browser plugin, an implementation
of Java Web Start (originally based on the Netx project) and a settings tool to
manage deployment settings for the aforementioned plugin and Web Start
implementations. 

%prep
%setup -q

%build
autoreconf -vfi
CXXFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS" \

export JAVA_HOME=/usr/lib/jvm/openjdk8

%configure \
    --with-jdk-home=${JAVA_HOME} \
    --disable-docs \
    --mandir=${JAVA_HOME}/man

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# icedteaweb-completion is currently not handled by make nor make install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/
cp icedteaweb-completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
desktop-file-install --vendor ''\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications javaws.desktop
desktop-file-install --vendor ''\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications itweb-settings.desktop
desktop-file-install --vendor ''\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications policyeditor.desktop

#not show in kde, use systemsettings module instead.
echo "NotShowIn=KDE;" >> $RPM_BUILD_ROOT%{_datadir}/applications/itweb-settings.desktop
echo "NotShowIn=KDE;" >> $RPM_BUILD_ROOT%{_datadir}/applications/policyeditor.desktop

#systemsettings modules.
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/kservices5/kcm_itwebsettings.desktop
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/kservices5/kcm_appletpolicyeditor.desktop


# install MetaInfo file for firefox
DESTDIR=%{buildroot} appstream-util install %{SOURCE1}

mkdir -p %{buildroot}%{_libdir}/mozilla/plugins/
pushd %{buildroot}%{_libdir}/mozilla/plugins/
ln -sd %{_libdir}/IcedTeaPlugin.so libjavaplugin.so
popd


%check
#make check
appstream-util validate $RPM_BUILD_ROOT/%{_datadir}/appdata/*.metainfo.xml

%post

%files
%defattr(-,root,root,-)
%{_sysconfdir}/bash_completion.d/
%{_prefix}/bin/*
%{_libdir}/IcedTeaPlugin.so
%{_libdir}/mozilla/plugins/libjavaplugin.so
%{_datadir}/applications/*
%{_datadir}/kservices5/kcm_itwebsettings.desktop
%{_datadir}/kservices5/kcm_appletpolicyeditor.desktop
%{_datadir}/icedtea-web

%{_libdir}/jvm/openjdk8/man/man1/*
%{_libdir}/jvm/openjdk8/man/cs/man1/*
%{_libdir}/jvm/openjdk8/man/de/man1/*
%{_libdir}/jvm/openjdk8/man/pl/man1/*
%{_datadir}/pixmaps/*
%{_datadir}/appdata/*.metainfo.xml
%doc NEWS README COPYING


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.6-3
- Rebuild

