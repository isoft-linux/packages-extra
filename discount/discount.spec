Name:           discount
Version:        2.1.8
Release:        3%{?dist}
Summary:        A command-line utility for converting Markdown files into HTML
License:        BSD
URL:            http://www.pell.portland.or.us/~orc/Code/%{name}
Source0:        %{url}/%{name}-%{version}.tar.gz
Patch0:         discount-ldconfig.patch
Requires:       libmarkdown%{?_isa} = %{version}-%{release}

%description
DISCOUNT is an implementation of John Gruber's Markdown language in C.
It includes all of the original Markdown features, along with a few
extensions, and passes the Markdown test suite.


%package -n libmarkdown
Summary: A fast implementation of the Markdown language in C

%description -n libmarkdown
libmarkdown is the library portion of discount, a fast Markdown language
implementation, written in C.


%package -n libmarkdown-devel
Summary: Development headers for the libmarkdown library
Requires: libmarkdown%{?_isa} = %{version}-%{release}

%description -n libmarkdown-devel
This package contains development headers and developer-oriented man pages for
libmarkdown.


%prep
%setup -q
%patch0


%build
CFLAGS='%{optflags}' ./configure.sh \
    --shared \
    --prefix=%{_prefix} \
    --execdir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-all-features \
    --with-fenced-code
make %{?_smp_mflags}


%install
make install.everything DESTDIR=%{buildroot}
# Rename sample programs (names are too generic) and matching man1 pages
mv %{buildroot}%{_bindir}/makepage %{buildroot}%{_bindir}/discount-makepage
mv %{buildroot}%{_bindir}/mkd2html %{buildroot}%{_bindir}/discount-mkd2html
mv %{buildroot}%{_bindir}/theme %{buildroot}%{_bindir}/discount-theme
mv %{buildroot}%{_mandir}/man1/makepage.1 \
   %{buildroot}%{_mandir}/man1/discount-makepage.1
mv %{buildroot}%{_mandir}/man1/mkd2html.1 \
   %{buildroot}%{_mandir}/man1/discount-mkd2html.1
mv %{buildroot}%{_mandir}/man1/theme.1 \
   %{buildroot}%{_mandir}/man1/discount-theme.1


%post -n libmarkdown -p /sbin/ldconfig
%postun -n libmarkdown -p /sbin/ldconfig


%check
make test


%files
%{_bindir}/markdown
%{_bindir}/discount-makepage
%{_bindir}/discount-mkd2html
%{_bindir}/discount-theme
%{_mandir}/man1/markdown.1*
%{_mandir}/man7/markdown.7*
%{_mandir}/man1/discount-*.1*
%{_mandir}/man7/mkd-*.7*


%files -n libmarkdown
%doc README COPYRIGHT CREDITS
%{_libdir}/libmarkdown.so.*


%files -n libmarkdown-devel
%{_libdir}/libmarkdown.so
%{_includedir}/mkdio.h
%{_mandir}/man3/markdown.3*
%{_mandir}/man3/mkd_*.3*
%{_mandir}/man3/mkd-*.3*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.1.8-3
- Rebuild

