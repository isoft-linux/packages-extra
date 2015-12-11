#prebuilt binary, no debuginfo
%define debug_package %{nil}

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g' -e 's!/usr/lib[^[:space:]]*/brp-python-hardlink.*$!!g')

Name: blender
Version: 2.76
Release: 2
Summary: 3D modeling, animation, rendering and post-production

License: GPLv2
URL: http://www.blender.org

#prebuilt x86_64 binary.
Source0: http://mirror.cs.umn.edu/blender.org/release/Blender2.76/blender-2.76b-linux-glibc211-x86_64.tar.bz2 

#desktop file
Source1: https://git.blender.org/gitweb/gitweb.cgi/blender.git/blob_plain/HEAD:/release/freedesktop/blender.desktop

#mime file
Source2: http://pkgs.fedoraproject.org/cgit/blender.git/plain/blender.xml 

#default settings for zh_CN locale, blender did not follow locale settings.
Source3: userpref.blend.zh_CN 

Source4: blender.sh

BuildRequires: sed tar

#not auto requires and provides.
AutoReqProv: no

%description
Blender is the essential software solution you need for 3D, from modeling,
animation, rendering and post-production to interactive creation and playback.

Professionals and novices can easily and inexpensively publish stand-alone,
secure, multi-platform content to the web, CD-ROMs, and other media.

%prep
%build
%install
#untar to dest dir.
mkdir -p %{buildroot}%{_datadir}/blender
tar jxf %{SOURCE0} -C %{buildroot}%{_datadir}/blender --strip-components=1

#put default config file for zh_CN to dest dir.
#it's not used by blender directly, but wrapper script will copy to ~/.config/blender/2.76/config/
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/blender/

#desktop
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/blender.desktop

#mime
#install -p -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/mime/packages/blender.xml

#wrapper
install -Dm0755 %{SOURCE4} %{buildroot}%{_bindir}/blender
sed -i 's|VERSION|%{version}|g' %{buildroot}%{_bindir}/blender

#icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/
cp -r %{buildroot}%{_datadir}/blender/icons/{16x16,22x22,32x32,48x48,256x256,scalable} %{buildroot}%{_datadir}/icons/hicolor/

#appdata file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: Long discussions with sergey on #blendercoders
BugReportURL: http://lists.blender.org/pipermail/bf-committers/2014-September/044217.html
SentUpstream: 2014-09-23
-->
<application>
  <id type="desktop">blender.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Blender provides a broad spectrum of modeling, texturing, lighting,
      animation and video post-processing functionality in one package.
      Through its open architecture, Blender provides cross-platform
      interoperability, extensibility, an incredibly small footprint, and a
      tightly integrated workflow.
      Blender is one of the most popular Open Source 3D graphics applications in
      the world.
    </p>
    <p>
      Aimed at media professionals and artists world-wide, Blender can be used
      to create 3D visualizations and still images, as well as broadcast- and
      cinema-quality videos, while the incorporation of a real-time 3D engine
      allows for the creation of 3D interactive content for stand-alone
      playback.
    </p>
  </description>
  <url type="homepage">http://www.blender.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/c.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/d.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/e.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/f.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/blender/g.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF


%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
#/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
#/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
#/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
#/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%{_bindir}/blender
%{_datadir}/applications/blender.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/*/*/*.svg

%dir %{_datadir}/blender
%{_datadir}/blender/*

#%{_datadir}/mime/packages/blender.xml
%{_datadir}/appdata/*.xml

%changelog
* Thu Dec 10 2015 Cjacker <cjacker@foxmail.com> - 2.76-2
- Initial build


