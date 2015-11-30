Name: winetricks 
Version: 20141130 
Release: 2
Summary: A package manager for win32 dlls and applications on posix

License: LGPL 
URL: http://kegel.com/wine/winetricks
Source0: http://kegel.com/wine/winetricks 

Requires: cabextract unrar unzip p7zip p7zip-plugins aria2 
Requires: perl sudo
#sha1sum
Requires: coreutils
Requires: xdg-utils
Requires: wine32

%description
Winetricks is a package manager for win32 dlls and applications on posix.
Features:
- Consists of a single shell script - no installation required
- Downloads packages automatically from original trusted sources
- Points out and works around known wine bugs automatically
- Both commandline and GUI operation
- Can install many packages in silent (unattended) mode
- Multiplatform; written for Linux, but supports MacOSX and Cygwin, too

%prep

%build
%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{SOURCE0} %{buildroot}%{_bindir}

%files
%{_bindir}/winetricks

%changelog
* Mon Nov 30 2015 Cjacker <cjacker@foxmail.com> - 20141130-2
- Initial build


