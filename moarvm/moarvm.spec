%global year 2015
%global month 09 


Name:           moarvm
Version:        0.%{year}.%{month}
Release:        2%{?dist}
Summary:        Meta-model On A Runtime Virtual Machine

License:        Artistic 2.0
URL:            http://moarvm.org
Source0:        http://moarvm.org/releases/MoarVM-%{year}.%{month}.tar.gz

BuildRequires:  libtommath-devel
# libuv-devel sha-devel
BuildRequires:  libatomic_ops-devel >= 7.4
BuildRequires:  perl(Pod::Usage) perl(ExtUtils::Command) perl(autodie)
#
BuildRequires:  discount



%description
Short for "Metamodel On A Runtime", MoarVM is a virtual machine built
especially for Rakudo Perl 6 and the NQP Compiler Toolchain. MoarVM is a 
backend for NQP.
MoarVM already stands out amongst the various Rakudo and NQP compilation
targets by typically:

    Running the Perl 6 specification test suite fastest
    Having the lowest memory usage
    Having the best startup time
    Being fastest to build both NQP and Rakudo - and thus in theory your
        Perl 6 and NQP programs too!


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
This package contains header files for developing applications that use
%{name} (Metamodel On A Runtime).



%prep
%setup -q -n MoarVM-%{year}.%{month}


%build
sed -i -e "/^\$config{cflags}/ s#.*#\$config{cflags} = \"$RPM_OPT_FLAGS -fPIC\";#" Configure.pl

# make sure to not bundle this
rm -r 3rdparty/msinttypes
# 3rdparty/libuv 3rdparty/sha1
# NQP do not build if MoarVM do not bundles sha
rm -r 3rdparty/libatomic_ops
#
# The upstream libtommath doesn't have the conversion from and to
# float/double that MoarVM needs. bn_mp_(get|set)_long.c are extentions of the
# origin libtommath source. The header files are needed to build.
rm `find 3rdparty/libtommath -type f ! -name '*long.c' -a ! -name '*.h'`

# --has-libuv --has-sha \
%{__perl} Configure.pl --prefix=%{_usr} --libdir=%{_libdir} --has-libtommath \
--has-libatomic_ops

make %{?_smp_mflags}

# Generate HTML files
for F in docs/*.markdown docs/*.md
do
   discount-mkd2html $F
done


%install
%make_install

# Force permissions on shared versioned libs so they get stripped
# and will provided.
chmod 755 $RPM_BUILD_ROOT%{_libdir}/libmoar.so

# Generating man-page
%{__perl} -MExtUtils::Command -e mkpath $RPM_BUILD_ROOT%{_mandir}/man1
pod2man --section=1 --name=moar docs/moar.pod | %{__gzip} -c > $RPM_BUILD_ROOT%{_mandir}/man1/moar.1.gz


%files
%doc LICENSE CREDITS docs
%{_bindir}/moar

%{_datadir}/nqp/lib/MAST
%{_libdir}/libmoar.so

%{_mandir}/man1/moar.1.gz


%files devel
%{_includedir}/dyncall
%{_includedir}/moar
%{_includedir}/tinymt
%{_datadir}/pkgconfig/moar.pc

%exclude %{_includedir}/libtommath
%exclude %{_includedir}/sha1
%exclude %{_includedir}/libuv
%exclude %{_includedir}/msinttypes



%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2015.09-2
- Rebuild

* Wed Oct 07 2015 Cjacker <cjacker@foxmail.com>
- initial build.

