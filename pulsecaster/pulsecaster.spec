%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pulsecaster
Version:        0.1.10
Release:        4%{?dist}
Summary:        A PulseAudio-based podcast recorder

Group:          Development/Languages
License:        GPLv3+
URL:            http://fedorahosted.org/pulsecaster
Source0:        http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
BuildRequires:  desktop-file-utils, gettext

Requires:       pulseaudio-libs >= 0.9.15
Requires:       pygobject3
Requires:       gstreamer >= 1.0
Requires:       dbus-python >= 0.83


%description
PulseCaster is a simple PulseAudio-based tool for making podcast
interviews. It is designed for ease of use and simplicity. The user
makes a call with a preferred PulseAudio-compatible Voice-over-IP
(VoIP) softphone application such as Ekiga or Twinkle, and then starts
PulseCaster to record the conversation to a multimedia file. The
resulting file can be published as a podcast or distributed in other
ways.

%prep
%setup -q


%build
%{__python} setup.py build
for F in po/*.po ; do
    L=`echo $F | %{__sed} 's@po/\([^\.]*\).po@\1@'`
    msgfmt -o po/$L.mo $F
done


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
desktop-file-install \
    --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
    %{name}.desktop
for D in ${RPM_BUILD_ROOT}%{_datadir}/locale/* ; do
    mv ${D}/LC_MESSAGES/*.mo ${D}/LC_MESSAGES/%{name}.mo
done
%find_lang %{name}

 
%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS README COPYING TODO
%{python_sitelib}/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/GConf/gsettings/*
%{_datadir}/appdata/*
%{_datadir}/glib-2.0/schemas/*


%changelog
* Thu Mar 24 2016 sulit <sulitsrc@163.com> - 0.1.10-4
- Init for isoft4

