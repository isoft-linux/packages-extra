Summary: A collection of Math symbol fonts 
Name:	 jsmath-fonts 
Version: 20090708 
Release: 2%{?dist}
# derived from computer modern metafont tex sources
License: Public domain 
Url: 	 http://www.math.union.edu/~dpvc/jsmath/welcome.html 
Source0: http://www.math.union.edu/~dpvc/jsmath/download/TeX-fonts-linux.tgz 
BuildArch: noarch

BuildRequires: fontpackages-devel
Requires: fontpackages-filesystem

%description
%{summary}.

%prep
%setup -q -n TeX-fonts-linux 

%build

%install
rm -rf %{buildroot}

# fonts
mkdir -p %{buildroot}%{_datadir}/fonts
install -p -m644 *.ttf %{buildroot}%{_datadir}/fonts

%clean
rm -rf %{buildroot}

%files
%{_datadir}/fonts/*.ttf

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 20090708-2
- Initial build

