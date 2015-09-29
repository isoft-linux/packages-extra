Name:       fbterm
Version:    1.7.0
Release:    1 
License:    GPLv2+
Group:      Core/Runtime/Utility 
URL:        http://code.google.com/p/fbterm/
Source0:    http://fbterm.googlecode.com/files/%{name}-%{version}.tar.gz
Summary:    A frame-buffer terminal emulator

BuildRequires: autoconf, automake
BuildRequires: fontconfig-devel
Requires: fontconfig

%description
FbTerm is a fast terminal emulator for Linux with frame-buffer device. 
Features include: 
- mostly as fast as terminal of Linux kernel while accelerated scrolling
  is enabled on frame-buffer device 
- select font with fontconfig and draw text with freetype2, same as 
  Qt/Gtk+ based GUI apps 
- dynamically create/destroy up to 10 windows initially running default
  shell 
- record scroll back history for every window 
- auto-detect text encoding with current locale, support double width 
  scripts like  Chinese, Japanese etc 
- switch between configurable additional text encodings with hot keys
  on the fly 
- copy/past selected text between windows with mouse when gpm server 
  is running


%prep
%setup -q -n %{name}-1.7

%build
%configure --enable-gpm
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%attr(4755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

