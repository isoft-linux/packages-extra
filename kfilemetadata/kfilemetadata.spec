
Name:    kfilemetadata
Summary: A library for extracting file metadata
Version: 4.14.3
Release: 4%{?dist}

# # KDE e.V. may determine that future LGPL versions are accepted
License: LGPLv2 or LGPLv3
URL:     https://projects.kde.org/projects/kde/kdelibs/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstream patches

BuildRequires: ebook-tools-devel
BuildRequires: kdelibs-devel >= %{version}
BuildRequires: pkgconfig(exiv2) >= 0.20
BuildRequires: pkgconfig(poppler-qt4)
BuildRequires: pkgconfig(taglib)

Requires: kdelibs%{?_isa}%{?_kde4_version: >= %{_kde4_version}}

%description
%{summary}.

%package devel
Summary:  Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs-devel
%description devel
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LGPL*
%{_kde4_libdir}/libkfilemetadata.so.4*
%{_kde4_libdir}/kde4/kfilemetadata_epubextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_exiv2extractor.so
%{_kde4_libdir}/kde4/kfilemetadata_odfextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_office2007extractor.so
%{_kde4_libdir}/kde4/kfilemetadata_officeextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_plaintextextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_popplerextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_taglibextractor.so
%{_kde4_libdir}/kde4/kfilemetadata_ffmpegextractor.so
%{_kde4_datadir}/kde4/services/kfilemetadata_ffmpegextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_epubextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_exiv2extractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_odfextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_office2007extractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_officeextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_plaintextextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_popplerextractor.desktop
%{_kde4_datadir}/kde4/services/kfilemetadata_taglibextractor.desktop
%{_kde4_datadir}/kde4/servicetypes/kfilemetadataextractor.desktop

%files devel
%{_kde4_includedir}/kfilemetadata/
%{_kde4_libdir}/libkfilemetadata.so
%{_kde4_libdir}/cmake/KFileMetaData

%changelog
