Name:    calligra-l10n 
Summary: Language files for calligra
Version: 2.9.8
Release: 3%{?dist}

License: GPLv2+
URL:     http://www.calligra-suite.org/

BuildArch: noarch
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif

Source0:http://download.kde.org/%{stable}/calligra-%{version}/calligra-l10n/calligra-l10n-ja-%{version}.tar.xz
Source1:http://download.kde.org/%{stable}/calligra-%{version}/calligra-l10n/calligra-l10n-zh_CN-%{version}.tar.xz
Source2:http://download.kde.org/%{stable}/calligra-%{version}/calligra-l10n/calligra-l10n-zh_TW-%{version}.tar.xz

Patch0: calligra-l10n-ja-fix-cmake.patch  
Patch1: calligra-l10n-zh_CN-fix-cmake.patch  
Patch2: calligra-l10n-zh_TW-fix-cmake.patch

Source1000: subdirs-calligra-l10n

## upstreamable patches

## upstream patches

BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  libxml2

%description
%{summary}.

%package ja
Summary:   Japanese language pack for calligra
Obsoletes: koffice-langpack-ja < %{koffice_obsoletes}
Requires:  %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description ja
%{summary}.

%package zh_CN
Summary:   Simplified Chinese language pack for calligra
Obsoletes: koffice-langpack-zh_CN < %{koffice_obsoletes}
Requires:  %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description zh_CN
%{summary}.

%package zh_TW
Summary:   Traditional Chinese language pack for calligra
Obsoletes: koffice-langpack-zh_TW < %{koffice_obsoletes}
Requires:  %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description zh_TW
%{summary}.


%prep
%setup -T -c -q -n %{name}-%{version}

for i in $(cat %{SOURCE1000}) ; do
  echo $i | grep -v '^#' && \
  %{__xz} -dc %{_sourcedir}/calligra-l10n-$i-%{version}.tar.xz | tar -xf -
done
pushd *-ja-*
%patch0 -p1
popd

pushd *-zh_CN-*
%patch1 -p1
popd

pushd *-zh_TW-*
%patch2 -p1
popd

%build
for calligra_lang in * ; do
  if [ -f $calligra_lang/CMakeLists.txt ]; then
    pushd $calligra_lang
     mkdir -p %{_target_platform}
     pushd %{_target_platform}
      %{cmake_kde4} .. 
      make %{?_smp_mflags}
     popd
    popd
  fi
done


%install
for calligra_lang in * ; do
  if [ -f $calligra_lang/CMakeLists.txt ]; then
    make install/fast DESTDIR=%{buildroot} -C $calligra_lang/%{_target_platform}
  fi
done

## unpackaged files
rm -rfv %{buildroot}%{_kde4_appsdir}/koffice/autocorrect

%files
#empty meta package

%files ja
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/*

%files zh_CN
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/*

%files zh_TW
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.9.8-3
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com> - 2.9.8-2
- Initial build

