Name: skype 
Version: 4.3.0.37
Release: 2
Summary: Skype is free Internet telephony that just works

License: Commercial 
URL: http://www.skype.com/products/skype/linux/
Source0: skype-4.3.0.37-fedora.i586.rpm

AutoReqProv: no
Requires: lib32-runtime 

%description
Wherever you are, wherever they are

Skype keeps you together. Call, see, message and share with others.
 * It's free to download and join.
 * Call, instant message and send photos and documents to anyone else on Skype.
 * And with a webcam you can catch up face-to-face with a video call.
 * Call mobiles and landlines worldwide at low rates.
 * Easily text message anywhere in the world.
 * Get your friends together on a conference call.

%prep

%build
%install
pushd %{buildroot}
rpm2cpio %{SOURCE0}|cpio -id
popd

rm -rf %{buildroot}/%{_sysconfdir}/prelink.conf.d

%files
%{_sysconfdir}/dbus-1/system.d/skype.conf
%{_bindir}/skype
%{_datadir}/applications/skype.desktop
%{_docdir}/skype-%{version}
%{_datadir}/icons/hicolor/*/apps/skype.*
%{_datadir}/pixmaps/skype.png
%dir %{_datadir}/skype
%{_datadir}/skype/*

%changelog
* Wed Dec 09 2015 Cjacker <cjacker@foxmail.com> - 4.3.0.37-2
- Initial build


