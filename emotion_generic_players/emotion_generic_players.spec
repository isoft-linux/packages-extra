Name:           emotion_generic_players
Version:        1.16.0
Release:        2%{?dist}
Summary:        Set of generic players for Emotion
License:        GPLv2+
Url:            http://enlightenment.org/
Source0:        http://download.enlightenment.org/rel/libs/emotion_generic_players/emotion_generic_players-%{version}.tar.gz

Requires:       efl
BuildRequires:  efl-devel
BuildRequires:  libvlc-devel

%description
Extra players for GPL players and unstable libraries.

%prep
%setup -q -n emotion_generic_players-%{version}

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install

%files
%doc ChangeLog README COPYING
%{_libdir}/emotion/generic_players

%changelog
* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.16.0-2
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.15.0-2
- Rebuild

