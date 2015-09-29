Name:	    openvanilla-modules	
Version:	0.9.1
Release:	1
Summary:    openvanilla modules	

Group:		Core/Runtime/Library
License:	GPLv2+
URL:		https://code.google.com/p/ucimf
Source0:	https://ucimf.googlecode.com/files/openvanilla-modules-%{version}.tar.gz

%description
%{summary}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_libdir}/openvanilla/OVIMGeneric.a
rpmclean
%files
%{_libdir}/openvanilla/OVIMGeneric.so
%dir %{_datadir}/openvanilla
%{_datadir}/openvanilla/*

%changelog

