# All package versioning is found here:
# the actual version is composed from these below, including leading 0 for release candidates
#   bzrmajor:  main bzr version
#   Version: bzr version, add subrelease version here
#   bzrrc: release candidate version, if any, line starts with % for rc, # for stable releas (no %).
#   release: rpm subrelease (0.N for rc candidates, N for stable releases)
%global bzrmajor 2.6
%global bzrminor .0
#global bzrrc b6
%global release 13

Name:           bzr
Version:        %{bzrmajor}%{?bzrminor}
Release:        %{release}%{?bzrrc:.}%{?bzrrc}%{?dist}
Summary:        Friendly distributed version control system

License:        GPLv2+
URL:            http://www.bazaar-vcs.org/
Source0:        https://launchpad.net/%{name}/%{bzrmajor}/%{version}%{?bzrrc}/+download/%{name}-%{version}%{?bzrrc}.tar.gz
Source1:        https://launchpad.net/%{name}/%{bzrmajor}/%{version}%{?bzrrc}/+download/%{name}-%{version}%{?bzrrc}.tar.gz.sig
Source2:        bzr-icon-64.png
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel zlib-devel bash-completion
# For building documents
BuildRequires:  python-sphinx
BuildRequires:  gettext
BuildRequires: Cython
Requires:   python-pycurl
Patch0:         bzr-locale-location.patch
Patch1:         bzr-match-hostname.patch

%description
Bazaar is a distributed revision control system that is powerful, friendly,
and scalable.  It is the successor of Baz-1.x which, in turn, was
a user-friendly reimplementation of GNU Arch.

%package doc
Summary:        Documentation for Bazaar
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains the documentation for the Bazaar version control system.

%prep
%setup -q -n %{name}-%{version}%{?bzrrc}
%patch0 -p1
%patch1 -p1

sed -i '1{/#![[:space:]]*\/usr\/bin\/\(python\|env\)/d}' bzrlib/_patiencediff_py.py
sed -i '1{/#![[:space:]]*\/usr\/bin\/\(python\|env\)/d}' bzrlib/weave.py

# Remove Cython generated .c files
find . -name '*_pyx.c' -exec rm \{\} \;

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

chmod a-x contrib/bash/bzrbashprompt.sh

# Build documents
make docs-sphinx

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --install-data %{_datadir} --root $RPM_BUILD_ROOT
chmod -R a+rX contrib
chmod 0644 contrib/debian/init.d
chmod 0644 contrib/bzr_ssh_path_limiter
chmod 0644 contrib/bzr_access
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/*.so

bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
install -Dpm 0644 contrib/bash/bzr $RPM_BUILD_ROOT$bashcompdir/bzr
rm contrib/bash/bzr

# This is included in %doc, remove redundancy here
#rm -rf $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/doc/

# Use independently packaged python-elementtree instead
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/util/elementtree/

# Install documents
install -d $RPM_BUILD_ROOT/%{_pkgdocdir}/pdf
cp -pr NEWS README TODO COPYING.txt contrib/ $RPM_BUILD_ROOT/%{_pkgdocdir}/
cd doc
for dir in *; do
    if [ -d $dir/_build/html ]; then
        cp -R $dir/_build/html $RPM_BUILD_ROOT%{_pkgdocdir}/$dir
        rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/$dir/.buildinfo 
        rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/$dir/_static/$dir/Makefile
        find $RPM_BUILD_ROOT%{_pkgdocdir}/$dir -name '*.pdf' | while read pdf; do
            ln $pdf $RPM_BUILD_ROOT%{_pkgdocdir}/pdf/
        done
    fi
done
cd ..

install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/pixmaps/bzr.png

%find_lang bzr

%clean
rm -rf $RPM_BUILD_ROOT


%files -f bzr.lang
%defattr(-,root,root,-)
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/NEWS
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/TODO
%doc %{_pkgdocdir}/COPYING.txt
%doc %{_pkgdocdir}/contrib/
%{_bindir}/bzr
%{_mandir}/man1/*
%{python_sitearch}/bzrlib/
%{_datadir}/bash-completion/
%{_datadir}/pixmaps/bzr.png
%{python_sitearch}/*.egg-info

%files doc
%defattr(-,root,root,-)
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/*
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README
%exclude %{_pkgdocdir}/TODO
%exclude %{_pkgdocdir}/COPYING.txt
%exclude %{_pkgdocdir}/contrib/

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.6.0-13
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
