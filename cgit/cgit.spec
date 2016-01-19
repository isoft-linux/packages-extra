# Review bug: https://bugzilla.redhat.com/479723

%global gitver      2.7.0
%global cachedir    %{_localstatedir}/cache/%{name}
%global filterdir   %{_libexecdir}/%{name}/filters
%global scriptdir   %{_localstatedir}/www/cgi-bin
%global cgitdata    %{_datadir}/%{name}

%global syntax_highlight 1

%global make_cgit \
export CFLAGS="%{optflags}" \
export LDFLAGS="%{?__global_ldflags}" \
make V=1 %{?_smp_mflags} \\\
     DESTDIR=%{buildroot} \\\
     INSTALL="install -p"  \\\
     CACHE_ROOT=%{cachedir} \\\
     CGIT_SCRIPT_PATH=%{scriptdir} \\\
     CGIT_SCRIPT_NAME=cgit \\\
     CGIT_DATA_PATH=%{cgitdata} \\\
     docdir=%{docdir} \\\
     filterdir=%{filterdir} \\\
     prefix=%{_prefix}

Name:           cgit
Version:        0.12
Release:        2%{?dist}
Summary:        A fast web interface for git

Group:          Development/Tools
License:        GPLv2
URL:            http://git.zx2c4.com/cgit/
Source0:        http://git.zx2c4.com/cgit/snapshot/%{name}-%{version}.tar.xz
Source1:        http://www.kernel.org/pub/software/scm/git//git-%{gitver}.tar.xz
Source2:        cgitrc
Source3:        README

%if %{syntax_highlight}
Patch1:         cgit-0.9.1-highlightv3.patch
BuildRequires:  highlight
%endif
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  asciidoc
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  lua-devel
BuildRequires:  libxml2

# Requires:       httpd-filesystem
# Requires:       webserver
Requires:       httpd


%description
Cgit is a fast web interface for git.  It uses caching to increase performance.

%prep
%setup -q -a 1
%if %{syntax_highlight}
%patch1 -p1
%endif

# setup the git dir
rm -rf git
mv git-%{gitver} git
sed -i 's|^\(CFLAGS = \).*|\1%{optflags}|' git/Makefile

# I tried to use matchpathcon, but we would need to require
# selinux-policy-targeted probably.

cgit_context=git_content_t
#cgit_context=httpd_sys_content_t

sed -e "s|@CGIT_CONTEXT@|$cgit_context|g" \
    %{SOURCE3} > README

cat > httpd.conf <<EOF
Alias /cgit-data /usr/share/cgit
ScriptAlias /cgit /var/www/cgi-bin/cgit
<Directory "/usr/share/cgit">
    Require all granted
</Directory>
EOF


%build
%{make_cgit}

# Something in the a2x chain doesn't like running in parallel. :/
%{make_cgit} -j1 doc-man doc-html

%if %{syntax_highlight}
highlight --print-style --style-outfile=stdout >> cgit.css
%endif


%install
rm -rf %{buildroot}
%{make_cgit} install install-man
install -d -m0755 %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cgitrc
install -p -m0644 httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/cgit.conf
install -d -m0755 %{buildroot}%{cachedir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README* *.html
%config(noreplace) %{_sysconfdir}/cgitrc
%config(noreplace) %{_sysconfdir}/httpd/conf.d/cgit.conf
%dir %attr(-,apache,root) %{cachedir}
%{cgitdata}
%{filterdir}
%{scriptdir}/*
%{_mandir}/man*/*


%changelog
* Tue Jan 19 2016 sulit <sulitsrc@gmail.com> - 0.12-2
- Init for isoft4
- add libxml2 buildrequire
