Name:           kamoso
Version:        3.0 
Release:        23%{?dist}
Summary:        Application for taking pictures and videos from a webcam

License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/multimedia/kamoso/
Source0:        http://download.kde.org/unstable/kamoso/kamoso-%{version}rc1.tar.xz

#we have no interest on share, since almost all website supported can not be access in China.
Patch0: kamoso-remove-purpose-require.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs-devel >= 4.6.0
# snapshot supports GST1 only
BuildRequires: pkgconfig(QtGStreamer-1.0)
BuildRequires: kf5-libkipi-devel


%description
Kamoso is an application to take pictures and videos out of your webcam.


%prep
%setup -n %{name}-%{version}rc1
%patch0 -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang kamoso --with-kde


%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.kamoso.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files -f kamoso.lang
/

%changelog
