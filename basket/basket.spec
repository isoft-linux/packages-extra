#NOTE, the version is 2.10b.

Name: basket
Summary: Note taking application
Version: 2.10
Release: 3%{?dist}

License: LGPLv2 or LGPLv3
URL: https://github.com/basket-notepads/basket
Source0: %{name}-%{version}b.tar.gz
Patch0: basket-tune-desktop.patch

BuildRequires: kdelibs-devel >= %{version}

%description
This multi-purpose note-taking application helps you to:

Easily take all sort of notes
Collect research results and share them
Centralize your project data and reuse it
Quickly organize your thoughts in idea boxes
Keep track of your information in a smart way
Make intelligent To Do lists
And a lot more...

%prep
%setup -q -n %{name}-%{version}b
%patch0 -p1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%find_lang basket

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f basket.lang
%{_bindir}/basket
%{_libdir}/kde4/basketthumbcreator.so
%{_libdir}/kde4/kcm_basket.so
%{_libdir}/libbasketcommon.so
%{_libdir}/libbasketcommon.so.4
%{_libdir}/libbasketcommon.so.4.14.12
%{_datadir}/applications/kde4/basket.desktop
%{_docdir}/HTML/en/basket
%{_datadir}/icons/hicolor/*/apps/basket.*
%{_datadir}/icons/hicolor/*/actions/*
%{_datadir}/kde4/apps/basket
%{_datadir}/kde4/services/*.desktop

%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build
