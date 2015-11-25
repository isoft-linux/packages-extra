Name:           binwalk
Version:        2.0.0
Release:        7%{?dist}
Summary:        Firmware analysis tool
License:        MIT
URL:            http://www.binwalk.org/
Source0:        https://github.com/devttys0/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         binwalk-2.0.0-unbundle-miniz.patch
Patch1:         binwalk-2.0.0-use-system-miniz.patch
Patch2:         binwalk-2.0.0-fix-binvis-python3.patch
BuildRequires:  python3-devel
BuildRequires:  miniz-devel
Requires:       file-libs
Suggests:       python3-pyqtgraph

%description
Binwalk is a tool for searching a given binary image for embedded files and
executable code. Specifically, it is designed for identifying files and code
embedded inside of firmware images. Binwalk uses the python-magic library, so 
it is compatible with magic signatures created for the Unix file utility. 

%prep
%autosetup -p1

%build
%configure --disable-bundles --with-python=%{__python3}
make %{?_smp_mflags}
chmod -c +x src/build/lib/binwalk/libs/*.so

%install
# Override --install-lib because package believes it is pure python but it
# actually contains arch-specific code.
%{__python3} setup.py install --install-lib=%{python3_sitearch} --prefix=%{_prefix} --root=%{buildroot}

%files
%doc API.md INSTALL.md README.md
%license LICENSE
%{_bindir}/%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}*.egg-info

%changelog
* Wed Nov 25 2015 sulit <sulitsrc@gmail.com> - 2.0.0-7
- init for isoft4
