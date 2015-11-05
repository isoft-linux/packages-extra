Name:           podofo
Version:        0.9.1
Release:        2%{?dist}
Summary:        Tools and libraries to work with the PDF file format

License:        GPLv2+
URL:            http://podofo.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         %{name}-0.9.1-unistd.patch
Patch1:         %{name}-0.9.1-lua52.patch
Patch2:         %{name}-0.9.1-freetype.patch

BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  cppunit-devel
BuildRequires:  lua-devel
BuildRequires:  doxygen


%description
PoDoFo is a library to work with the PDF file format. The name comes from
the first letter of PDF (Portable Document Format). A few tools to work
with PDF files are already included in the PoDoFo package.

The PoDoFo library is a free, portable C++ library which includes classes
to parse PDF files and modify their contents into memory. The changes can be
written back to disk easily. The parser can also be used to extract
information from a PDF file (for example the parser could be used in a PDF
viewer). Besides parsing PoDoFo includes also very simple classes to create
your own PDF files. All classes are documented so it is easy to start writing
your own application using PoDoFo.


%package libs
Summary:        Runtime library for %{name}
License:        LGPLv2+

%description libs
Runtime library for %{name}.


%package devel
Summary:        Development files for %{name} library
License:        LGPLv2+
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Development files and documentation for the %{name} library.


%prep
%setup -q
%patch0 -p1 -b .unistd
%patch1 -p1 -b .lua52
%patch2 -p1 -b .freetype

# disable timestamps in docs
echo "HTML_TIMESTAMP = NO" >> Doxyfile

# switch to system provided files
rm cmake/modules/FindFREETYPE.cmake
rm cmake/modules/FindZLIB.cmake


%build
%cmake -DPODOFO_BUILD_SHARED=1 .
make %{?_smp_mflags}

# build the docs
doxygen

# set timestamps on generated files to some constant
find doc/html -exec touch -r %{SOURCE0} {} \;


%install
make install DESTDIR=$RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc COPYING
%{_bindir}/%{name}*
%{_mandir}/man1/%{name}*.1*

%files libs
%doc AUTHORS COPYING.LIB ChangeLog FAQ.html README.html TODO
%{_libdir}/*.so.*

%files devel
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/*.so


%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.9.1-2
- Initial build

