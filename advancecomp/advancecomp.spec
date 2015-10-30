Name:           advancecomp
Version:        1.20
Release:        2%{?dist}
Summary:        Recompression utilities for .PNG, .MNG and .ZIP files
License:        GPLv3
URL:            http://advancemame.sourceforge.net/
Source0:        http://downloads.sf.net/advancemame/advancecomp-%{version}.tar.gz
BuildRequires:  tofrodos
BuildRequires:  zlib-devel

%description
AdvanceCOMP is a set of recompression utilities for .PNG, .MNG and .ZIP files.
The main features are :
* Recompress ZIP, PNG and MNG files using the Deflate 7-Zip implementation.
* Recompress MNG files using Delta and Move optimization.

This package contains:
* advzip - Recompression and test utility for zip files
* advpng - Recompression utility for png files
* advmng - Recompression utility for mng files
* advdef - Recompression utility for deflate streams in .png, .mng and .gz 
files

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make check

%files
%license COPYING
%doc AUTHORS HISTORY README
%doc doc/{advdef*,authors,history,readme}.{txt,html}
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.20-2
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.

