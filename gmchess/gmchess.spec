Name: gmchess
Version: 0.29.6
Release: 2%{?dist}
Summary: Chinese chess

License: GPLv2
URL: http://gmchess.googlecode.com
Source0: http://gmchess.googlecode.com/files/gmchess-0.29.6.tar.bz2
Patch0: gmchess-tune-desktop.patch

BuildRequires: gtkmm2-devel gettext

%description
GMChess is a free program that plays the game of Chinese Chess (Xiangqi).

%prep
%setup -q 
%patch0 -p1

%build
export CXXFLAGS="-std=c++11"
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%{_datadir}/applications/gmchess.desktop
%{_datadir}/gmchess
%{_datadir}/man/man6/*.gz
%{_datadir}/pixmaps/gmchess.png
%{_libdir}/libeval.so.*
%{_bindir}/convert_pgn
%{_bindir}/eleeye_engine
%{_bindir}/gmchess

%exclude %{_libdir}/libeval.la 
%exclude %{_libdir}/libeval.so

%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- Initial package

