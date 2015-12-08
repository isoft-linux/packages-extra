%define debug_package %{nil}

# we are shipping the full contents of src in the data subpackage, which
# contains binary-like things (ELF data for tests, etc)
%global _binaries_in_noarch_packages_terminate_build 0

# Do not check any files in doc or src for requires
%global __requires_exclude_from ^(%{_datadir}|/usr/lib)/%{name}/(doc|src)/.*$

# Don't alter timestamps of especially the .a files (or else go will rebuild later)
# Actually, don't strip at all since we are not even building debug packages and this corrupts the dwarf testdata
%global __strip /bin/true

# rpmbuild magic to keep from having meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

# let this match the macros in macros.golang
%global goroot          /usr/lib/%{name}
%global gopath          %{_datadir}/gocode
%global go_arches       %{ix86} x86_64 %{arm}

%ifarch x86_64
%global gohostarch  amd64
%endif
%ifarch %{ix86}
%global gohostarch  386
%endif
%ifarch %{arm}
%global gohostarch  arm
%endif

%global go_api 1.5
%global go_version 1.5.2

Name:           golang
Version:        1.5
Release:        7%{?dist}
Summary:        The Go Programming Language

License:        BSD
URL:            http://golang.org/
Source0:        https://storage.googleapis.com/golang/go%{go_version}.src.tar.gz

Source100:      golang-gdbinit
Source101:      golang-prelink.conf
Source102:      macros.golang

Patch210:       golang-hostname.patch
# use the arch dependent path in the bootstrap
Patch212:       golang-1.5-bootstrap-binary-path.patch
# disable TestGdbPython
# https://github.com/golang/go/issues/11214
Patch213:       go1.5beta1-disable-TestGdbPython.patch
# disable  TestCloneNEWUSERAndRemapNoRootDisableSetgroups
# this is not possible in the limitied build chroot
Patch214:       go1.5beta2-disable-TestCloneNEWUSERAndRemapNoRootDisableSetgroups.patch


ExclusiveArch:  %{go_arches}

BuildRequires:  golang > 1.4
BuildRequires:  /usr/bin/hostname

Provides:       go = %{version}-%{release}
Requires:       %{name}-bin
Requires:       %{name}-src = %{version}-%{release}



%description
%{summary}.


%package       docs
Summary:       Golang compiler docs
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch
Obsoletes:     %{name}-docs < 1.1-4

%description   docs
%{summary}.

%package       misc
Summary:       Golang compiler miscellaneous sources
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   misc
%{summary}.

%package       tests
Summary:       Golang compiler tests for stdlib
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   tests
%{summary}.

##
# the source tree
%package        src
Summary:        Golang compiler source tree
BuildArch:      noarch
%description    src
%{summary}

%package        bin
Summary:        Golang core compiler tools
Requires:       go = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

Requires:       glibc
Requires:       gcc
%description    bin
%{summary}

# Workaround old RPM bug of symlink-replaced-with-dir failure
%pretrans -p <lua>
for _,d in pairs({"api", "doc", "include", "lib", "src"}) do
  path = "%{goroot}/" .. d
  if posix.stat(path, "type") == "link" then
    os.remove(path)
    posix.mkdir(path)
  end
end


%prep
%setup -q -n go
%patch210 -p0
%patch212 -p1
%patch213 -p1
%patch214 -p1

%build
# go1.5 bootstrapping. The compiler is written in golang.
export GOROOT_BOOTSTRAP=%{goroot}

# set up final install location
export GOROOT_FINAL=%{goroot}

# TODO use the system linker to get the system link flags and build-id
# when https://code.google.com/p/go/issues/detail?id=5221 is solved
#export GO_LDFLAGS="-linkmode external -extldflags $RPM_LD_FLAGS"

export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}

pushd src
# use our gcc options for this build, but store gcc as default for compiler
CFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="$RPM_LD_FLAGS" \
CC="gcc" \
CC_FOR_TARGET="gcc" \
GOOS=linux \
GOARCH=%{gohostarch} \
	./make.bash --no-clean
popd

%install
rm -rf $RPM_BUILD_ROOT

# create the top level directories
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{goroot}

# install everything into libdir (until symlink problems are fixed)
# https://code.google.com/p/go/issues/detail?id=5830
cp -apv api bin doc favicon.ico lib pkg robots.txt src misc VERSION \
   $RPM_BUILD_ROOT%{goroot}

# bz1099206
find $RPM_BUILD_ROOT%{goroot}/src -exec touch -r $RPM_BUILD_ROOT%{goroot}/VERSION "{}" \;
# and level out all the built archives
touch $RPM_BUILD_ROOT%{goroot}/pkg
find $RPM_BUILD_ROOT%{goroot}/pkg -exec touch -r $RPM_BUILD_ROOT%{goroot}/pkg "{}" \;
# generate the spec file ownership of this source tree and packages
cwd=$(pwd)
src_list=$cwd/go-src.list
pkg_list=$cwd/go-pkg.list
misc_list=$cwd/go-misc.list
docs_list=$cwd/go-docs.list
tests_list=$cwd/go-tests.list
rm -f $src_list $pkg_list $docs_list $misc_list $tests_list
touch $src_list $pkg_list $docs_list $misc_list $tests_list
pushd $RPM_BUILD_ROOT%{goroot}
	find src/ -type d ! -ipath '*/testdata/*' -printf '%%%dir %{goroot}/%p\n' >> $src_list
	find src/ ! -type d ! -ipath '*/testdata/*' ! -name '*_test.go' -printf '%{goroot}/%p\n' >> $src_list

	find bin/ pkg/ -type d -printf '%%%dir %{goroot}/%p\n' >> $pkg_list
	find bin/ pkg/ ! -type d -printf '%{goroot}/%p\n' >> $pkg_list

	find doc/ -type d -printf '%%%dir %{goroot}/%p\n' >> $docs_list
	find doc/ ! -type d -printf '%{goroot}/%p\n' >> $docs_list

	find misc/ -type d -printf '%%%dir %{goroot}/%p\n' >> $misc_list
	find misc/ ! -type d -printf '%{goroot}/%p\n' >> $misc_list

	find src/ -type d -ipath '*/testdata/*' -printf '%%%dir %{goroot}/%p\n' >> $tests_list
	find src/ ! -type d -ipath '*/testdata/*' -o -name '*_test.go' -printf '%{goroot}/%p\n' >> $tests_list
popd

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv $RPM_BUILD_ROOT%{goroot}/lib/time

# remove the doc Makefile
rm -rfv $RPM_BUILD_ROOT%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p $RPM_BUILD_ROOT%{goroot}/bin/linux_%{gohostarch}
ln -sf %{goroot}/bin/go $RPM_BUILD_ROOT%{goroot}/bin/linux_%{gohostarch}/go
ln -sf %{goroot}/bin/gofmt $RPM_BUILD_ROOT%{goroot}/bin/linux_%{gohostarch}/gofmt

# ensure these exist and are owned
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/github.com/
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/bitbucket.org/
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/code.google.com/
mkdir -p $RPM_BUILD_ROOT%{gopath}/src/code.google.com/p/

# make sure these files exist and point to alternatives
rm -f $RPM_BUILD_ROOT%{_bindir}/go
ln -sf /etc/alternatives/go $RPM_BUILD_ROOT%{_bindir}/go
rm -f $RPM_BUILD_ROOT%{_bindir}/gofmt
ln -sf /etc/alternatives/gofmt $RPM_BUILD_ROOT%{_bindir}/gofmt

# gdbinit
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
cp -av %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d/golang.gdb

# prelink blacklist
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
cp -av %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d/golang.conf

# rpm macros
mkdir -p %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cp -av %{SOURCE102} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.golang


%check
export GOROOT=$(pwd -P)
export PATH="$GOROOT"/bin:"$PATH"
cd src
CC="gcc" \
CFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="$RPM_LD_FLAGS" \
./run.bash --no-rebuild -v -k ||:
cd ..


%post bin
%{_sbindir}/update-alternatives --install %{_bindir}/go \
	go %{goroot}/bin/go 90 \
	--slave %{_bindir}/gofmt gofmt %{goroot}/bin/gofmt

%preun bin
if [ $1 = 0 ]; then
	%{_sbindir}/update-alternatives --remove go %{goroot}/bin/go
fi


%files
%doc AUTHORS CONTRIBUTORS LICENSE PATENTS
# VERSION has to be present in the GOROOT, for `go install std` to work
%doc %{goroot}/VERSION
%dir %{goroot}/doc
%doc %{goroot}/doc/*

# go files
%dir %{goroot}
%exclude %{goroot}/bin/
%exclude %{goroot}/pkg/
%exclude %{goroot}/src/
%exclude %{goroot}/doc/
%exclude %{goroot}/misc/
%{goroot}/*

# ensure directory ownership, so they are cleaned up if empty
%dir %{gopath}
%dir %{gopath}/src
%dir %{gopath}/src/github.com/
%dir %{gopath}/src/bitbucket.org/
%dir %{gopath}/src/code.google.com/
%dir %{gopath}/src/code.google.com/p/


# gdbinit (for gdb debugging)
%{_sysconfdir}/gdbinit.d

# prelink blacklist
%{_sysconfdir}/prelink.conf.d

%{_rpmconfigdir}/macros.d/macros.golang


%files -f go-src.list src

%files -f go-docs.list docs

%files -f go-misc.list misc

%files -f go-tests.list tests

%files -f go-pkg.list bin
%{_bindir}/go
%{_bindir}/gofmt


%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.5-7
- Update to 1.5.2

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.5-6
- Rebuild

* Thu Aug 20 2015 Cjacker <cjacker@foxmail.com>
- update to 1.5.
* Fri Aug 07 2015 Cjacker <cjacker@foxmail.com>
- update to 1.5rc1
