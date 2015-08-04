Summary:	A library for generating Enhanced Metafiles
Summary(pl):	Biblioteka do generowania plików w formacie Enhanced Metafile
Name:		libEMF
Version:	1.0.7
Release:	9
License:	LGPLv2+ and GPLv2+
URL:		http://libemf.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/libemf/libemf/%{version}/libEMF-%{version}.tar.gz
Patch0:		libEMF-aarch64.patch
BuildRequires:	libstdc++-devel

%description
libEMF is a library for generating Enhanced Metafiles on systems which
don't natively support the ECMA-234 Graphics Device Interface
(GDI). The library is intended to be used as a driver for other
graphics programs such as Grace or gnuplot. Therefore, it implements a
very limited subset of the GDI.

%description -l pl
libEMF to biblioteka do generowania plików w formacie Enhanced
Metafile na systemach nie obsługujących natywnie systemu graficznego
ECMA-234 GDI. Biblioteka ma służyć jako sterownik dla innych programów
graficznych, takich jak Grace czy gnuplot. Z tego powodu ma
zaimplementowany bardzo ograniczony podzbiór GDI.

%package devel
Summary:	libEMF header files
Summary(pl):	Pliki nagłówkowe libEMF
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
libEMF header files.

%description devel -l pl
Pliki nagłówkowe libEMF.

%prep
%setup -q
%patch0 -p1 -b .aarch64

%build
%configure \
	--disable-static \
	--enable-editing

make %{?_smp_mflags}

%install
export CPPROG="cp -p"
make install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libEMF.la

%check
make check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING COPYING.LIB NEWS README
%{_bindir}/*
%{_libdir}/lib*.so.*

%files devel
%doc doc/html
%{_libdir}/lib*.so
%{_includedir}/libEMF

%changelog
