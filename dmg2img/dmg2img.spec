%define debug_package %{nil}
Name: dmg2img 
Version: 1.6.5
Release: 2
Summary: DMG2IMG is an Apple's compressed dmg to standard (hfsplus) image disk file convert tool. 

License: unknown
URL: http://vu1tur.eu.org/tools/
Source0: http://vu1tur.eu.org/tools/dmg2img-%{version}.tar.gz

BuildRequires: zlib-devel bzip2-devel

%description
%{summary}

%prep
%setup -q

%build
make


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 dmg2img %{buildroot}%{_bindir}

%files
%{_bindir}/dmg2img

%changelog
* Sun Dec 13 2015 Cjacker <cjacker@foxmail.com> - 1.6.5-2
- Initial build


