Name:           pencil
Version:        2.0.5
Release:        5%{?dist}
Summary:        A sketching and GUI prototyping tool
License:        GPLv2
URL:            http://code.google.com/p/evoluspencil/
Source0:        http://evoluspencil.googlecode.com/files/%{name}-%{version}.tar.gz

Requires:       xulrunner >= 1.9.8
BuildRequires:  desktop-file-utils
BuildArch:      noarch

%description
Pencil is an open source GUI prototyping and sketching tools released under GPL.


%prep
%setup -q

%build

%install
mkdir -p $RPM_BUILD_ROOT
cp -R usr $RPM_BUILD_ROOT
desktop-file-install \
--add-category="AudioVideo" \
--delete-original \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop


%files
%doc COPYING
%{_datadir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0.5-5
- Rebuild

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 2.0.5-4
- Initial build

