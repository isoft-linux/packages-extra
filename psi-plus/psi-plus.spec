%global rev 20141205git440
%global rev_l10n 52f378a
%global genericplugins attentionplugin autoreplyplugin birthdayreminderplugin captchaformsplugin chessplugin cleanerplugin clientswitcherplugin conferenceloggerplugin contentdownloaderplugin extendedmenuplugin extendedoptionsplugin gmailserviceplugin gomokugameplugin historykeeperplugin icqdieplugin imageplugin jabberdiskplugin juickplugin pepchangenotifyplugin qipxstatusesplugin screenshotplugin skinsplugin stopspamplugin storagenotesplugin translateplugin videostatusplugin watcherplugin gnupgplugin otrplugin
%global unixplugins gnome3supportplugin
%global devplugins pstoplugin

Summary:        Jabber client based on Qt
Name:           psi-plus
Version:        0.16
Release:        0.23.%{rev}%{?dist}
Epoch:          1

URL:            http://code.google.com/p/psi-dev/
# GPLv2+ - core of Psi+
# LGPLv2.1+ - iris library, Psi+ widgets, several Psi+ tools
# zlib/libpng - UnZip 0.15 additionnal library
License:        GPLv2+ and LGPLv2+ and zlib
# Sources is latest snapshot from git://github.com/psi-im/psi.git with applyed all worked patches from psi-dev team.
# Sources also include plugins. There isn't development files therefore plugin interface very unstable.
# So i can't split plugins to separate package. I need to maintain it together.
Source0:        http://files.psi-plus.com/sources/%{name}-%{version}-%{rev}.tar.bz2
# Translation from  https://github.com/psi-plus/psi-plus-l10n
Source1:        http://files.psi-plus.com/sources/%{name}-l10n-%{rev_l10n}.tar.bz2
# I use this script to make tarballs with Psi+ sources and translations
Source2:        generate-tarball.sh

Patch0:         psi-plus-psimedia.patch
Patch1:         psi-new-history.patch

BuildRequires:  pkgconfig(QtCore)
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  pkgconfig(QtSvg)
BuildRequires:  pkgconfig(QtXml)
BuildRequires:  pkgconfig(QtXmlPatterns)
BuildRequires:  pkgconfig(QtNetwork)
BuildRequires:  pkgconfig(QtDBus)
BuildRequires:  pkgconfig(QtSql)
BuildRequires:  pkgconfig(QtScript)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(QJson)
# qjdns ABI changes
%if 0%{?rhel} > 7 || 0%{?fedora} > 22
BuildRequires:  pkgconfig(qjdns-qt4)
%else
BuildRequires:  pkgconfig(qjdns)
%endif
BuildRequires:  pkgconfig(enchant)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(qca2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libotr)
BuildRequires:  pkgconfig(libidn)

BuildRequires:  desktop-file-utils
BuildRequires:  qconf >= 1.4-2
BuildRequires:  gettext
BuildRequires:  libtidy-devel

Requires:       %{name}-common = %{epoch}:%{version}-%{release}
Requires:       sox%{?_isa}
Requires:       gnupg
# Required for SSL/TLS connections
Requires:       qca-ossl%{?_isa}

# epel7 has no qca-gnupg package
%if 0%{?rhel} != 7
# Required for GnuPG encryption
Requires:       qca-gnupg%{?_isa}
%endif

# hicolor-icon-theme is owner of themed icons folders
Requires:       hicolor-icon-theme

# New Fedora rules allow to use bundled libraries
# https://bugzilla.redhat.com/show_bug.cgi?id=737304#c15
Provides:       bundled(iris)

%description
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru

%package        i18n
Summary:        Language packs for Psi
Requires:       %{name} = %{epoch}:%{version}-%{release}
BuildArch:      noarch

%description    i18n
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru
This package adds internationalization to Psi+.

%package        common
Summary:        Noarch resources for Psi+
BuildArch:      noarch

%description    common
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru
This package contains huge of base mandatory resources for Psi+.

%package        plugins
Summary:        Plugins pack for Psi+
# GPLv2 is used for the most plugins
# BSD - screenshot plugin
# Beerware - icqdie plugin
License:        GPLv2+ and BSD and Beerware
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
# Filter out plugins from provides
%global __provides_exclude_from ^%{_libdir}/psi-plus


%description    plugins
Psi+ - Psi IM Mod by psi-dev@conference.jabber.ru

 * Attention Plugin
This plugin is designed to send and receive special messages such as
Attentions.

 * Autoreply Plugin
This plugin acts as an auto-answering machine.

 * Birthday Reminder Plugin
This plugin is designed to show reminders of upcoming birthdays.

 * Captcha Forms Plugin
This plugin is designed to pass of captcha directly from the Psi+.

 * Chess Plugin
This plugin allows you to play chess with your friends.
The plugin is compatible with a similar plugin for Tkabber.

 * Cleaner Plugin
This plugin is designed to clear the avatar cache, saved local copies
of vCards and history logs.

 * Client Switcher Plugin
This plugin is intended to spoof version of the Jabber client, the
name and type of operating system. It is possible to manually specify
the version of the client and the operating system or choose from a
predefined list.

 * Conference Logger Plugin
This plugin is designed to save conference logs in which the Psi+
user sits.

 * Content Downloader Plugin
This plugin can currently be used to download and install roster
iconsets and emoticons.

 * Extended Menu Plugin
This plugin adds roster submenu 'Extended Actions' to contact's
context menu. At the moment we have the following items: 'Copy JID',
'Copy the nickname', 'Copy the status message' and 'Ping'.

 * Extended Options Plugin
This plugin is designed to allow easy configuration of some advanced
options in Psi+. This plugin gives you access to advanced application
options, which do not have a graphical user interface.

 * Gmail Service Plugin
Shows notifications of new messages in your Gmailbox.

 * History Keeper Plugin
This plugin is designed to remove the history of selected contacts
when the Psi+ is closed.

 * ICQ Must Die Plugin
This plugin is designed to help you transfer as many contacts as
possible from ICQ to Jabber.

 * Image Plugin
This plugin is designed to send images to roster contacts.

 * Juick Plugin
This plugin is designed to work efficiently and comfortably with the
Juick microblogging service.

 * PEP Change Notify Plugin
The plugin is designed to display popup notifications on change of
moods, activities and tunes at the contacts of the roster. In the
settings you can choose which ones to include notification of events,
specify the time within which a notice will appear, as well as play a
sound specify.

 * Qip X-statuses Plugin
This plugin is designed to display X-statuses of contacts using the
QIP Infium jabber client.

 * Screenshot Plugin
This plugin allows you to make a snapshot (screenshot) of the screen,
edit the visible aria to make a screenshot and save the image to a
local drive or upload to HTTP/FTP server.

 * Stop Spam Plugin
This plugin is designed to block spam messages and other unwanted
information from Psi+ users.

 * Storage Notes Plugin
This plugin is an implementation of XEP-0049: Private XML Storage.
The plugin is fully compatible with notes saved using Miranda IM.
The plugin is designed to keep notes on the jabber server with the
ability to access them from anywhere using Psi+ or Miranda IM.

 * Translate Plugin
This plugin allows you to convert selected text into another language.

 * Video Status Changer Plugin
This plugin is designed to set the custom status when you see the
video in selected video player. Communication with players made by
D-Bus.

 * Skins Plugin
This plugin is designed to create, store and apply skins to Psi+.

 * Off-the-Record Messaging Plugin
a cryptographic protocol that provides strong encryption for instant
messaging conversations. OTR uses a combination of the AES
symmetric-key algorithm, the Diffie–Hellman key exchange, and the SHA-1
hash function. In addition to authentication and encryption, OTR
provides perfect forward secrecy and malleable encryption.

 * PSTO Plugin
Instant bloging service.

 * GnuPG Plugin
A front end for gpg. Allow to handle keys.

%prep
%setup -q -n %{name}-%{version}-%{rev}
%patch0 -p1
%patch1 -p1

# fix rpmlint spurious-executable-perm
find . -name '*.cpp' -or -name '*.h' | xargs chmod 644

# Remove bundled libraries
rm -fr src/libpsi/tools/zip/minizip
rm -fr iris/src/jdns

# Psi+ always uses last iris version. So I need to provide bundled
# iris to guarantee efficiency of program.
# rm -fr iris

# Untar russian language
%{__tar} xjf %{SOURCE1} -C .

%build
unset QTDIR
qconf-qt4
./configure                        \
        --prefix=%{_prefix}        \
        --bindir=%{_bindir}        \
        --libdir=%{_libdir}        \
        --datadir=%{_datadir}      \
        --release                  \
        --no-separate-debug-info   \
        --enable-webkit            \
        --enable-plugins           \
        --enable-whiteboarding     \
        --psimedia-path=%{_libdir}/psi/plugins/libgstprovider.so

make %{?_smp_mflags}

pushd translations
lrelease-qt4 *.ts
popd

pushd src/plugins

# Make paths for generic plugins
allplugins=""
for dir in %{genericplugins}
do
  allplugins="${allplugins} generic/$dir"
done

# Make paths for unix plugins
for dir in %{unixplugins}
do
  allplugins="${allplugins} unix/$dir"
done

# Make paths for dev plugins
for dir in %{devplugins}
do
  allplugins="${allplugins} dev/$dir"
done

# Compile all plugins
for dir in ${allplugins}
do
  pushd $dir
  %{_qt4_qmake}
  make %{?_smp_mflags}
  popd
done
popd

%install
# Qt doesn't understand DESTDIR. So I need to use INSTALL_ROOT instead of.
# %%make_install can't be used here.
INSTALL_ROOT=$RPM_BUILD_ROOT make install

# README and COPYING must be holds in doc dir. See %%doc tag in %%files
rm $RPM_BUILD_ROOT%{_datadir}/psi-plus/README
rm $RPM_BUILD_ROOT%{_datadir}/psi-plus/COPYING

# Install languages
cp -p translations/*.qm $RPM_BUILD_ROOT%{_datadir}/%{name}
%find_lang psi --with-qt

mkdir -p $RPM_BUILD_ROOT%{_libdir}/psi-plus/plugins

# Make paths for generic plugins
allplugins=""
for dir in %{genericplugins}
do
  allplugins="${allplugins} generic/$dir"
done

# Make paths for unix plugins
for dir in %{unixplugins}
do
  allplugins="${allplugins} unix/$dir"
done

# Make paths for dev plugins
for dir in %{devplugins}
do
  allplugins="${allplugins} dev/$dir"
done

pushd src/plugins

# Install all plugins
for dir in ${allplugins}
do
  install -p -m 0755 $dir/*.so $RPM_BUILD_ROOT%{_libdir}/psi-plus/plugins/
done
popd

%check
# Menu file is being installed when make install
# so it need only to check this allready installed file
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/psi-plus.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license COPYING
%doc README
%{_bindir}/psi-plus
%{_datadir}/applications/psi-plus.desktop
%{_datadir}/icons/hicolor/*/apps/psi-plus.png

%files i18n -f psi.lang

%files plugins
%{_libdir}/psi-plus

%files common
%license COPYING
%dir %{_datadir}/psi-plus
%{_datadir}/psi-plus/*
%exclude %{_datadir}/psi-plus/*.qm

%changelog
* Wed Dec 02 2015 sulit <sulitsrc@gmail.com> - 1:0.16-0.23.20141205git440
- Init for isoft4
