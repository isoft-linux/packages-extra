Name:           optipng
Version:        0.7.5
Release:        6%{?dist}
Summary:        PNG optimizer and converter

License:        zlib
URL:            http://optipng.sourceforge.net/
Source0:        http://downloads.sourceforge.net/optipng/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel libpng-devel

%description
OptiPNG is a PNG optimizer that recompresses image files to a smaller size,
without losing any information. This program also converts external formats
(BMP, GIF, PNM and TIFF) to optimized PNG, and performs PNG integrity checks
and corrections.


%prep
%setup -q
for f in AUTHORS.txt doc/history.txt ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done

# Ensure system libs and headers are used; as of 0.6.3 pngxtern will use
# the bundled headers if present even with -with-system-*, causing failures.
rm -rf src/libpng src/zlib


%build
./configure -prefix=%{_prefix} -mandir=%{_mandir} \
    -with-system-zlib -with-system-libpng
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod -c 755 $RPM_BUILD_ROOT%{_bindir}/optipng


%check
make test CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc AUTHORS.txt README.txt doc/*
%{_bindir}/optipng
%{_mandir}/man1/optipng.1*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.7.5-6
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
