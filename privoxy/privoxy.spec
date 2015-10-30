%define privoxyconf %{_sysconfdir}/%{name}
%define privoxy_uid 73
%define privoxy_gid 73
%define beta_or_stable stable
#define beta_or_stable beta

Name: privoxy
Version: 3.0.23
Release: 3%{?dist}
Summary: Privacy enhancing proxy
License: GPLv2+
Source0: http://downloads.sourceforge.net/ijbswa/%{name}-%{version}-%{beta_or_stable}-src.tar.gz
Source1: privoxy.service
Source2: privoxy.logrotate
#Patch0:  privoxy-3.0.16-chkconfig.patch
#Patch1:  privoxy-3.0.16-configdir.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://www.privoxy.org/
Requires(pre): shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: libtool autoconf pcre-devel zlib-devel systemd

%description 
Privoxy is a web proxy with advanced filtering capabilities for
protecting privacy, filtering web page content, managing cookies,
controlling access, and removing ads, banners, pop-ups and other
obnoxious Internet junk. Privoxy has a very flexible configuration and
can be customized to suit individual needs and tastes. Privoxy has application
for both stand-alone systems and multi-user networks.

Privoxy is based on the Internet Junkbuster.

%prep
%setup -q -n %{name}-%{version}-%{beta_or_stable}
#%patch0 -p1
#%patch1 -p1

%build
rm -rf autom4te.cache
autoreconf
# lets test how it works with dynamic pcre:
#configure --disable-dynamic-pcre
%configure
make %{?_smp_mflags}


%install
/bin/rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}%{_localstatedir}/log/%{name} \
         %{buildroot}%{privoxyconf}/templates \
         %{buildroot}%{_unitdir}
# Upstream dropped this one:
#         %{buildroot}%{_sysconfdir}/logrotate.d

install -p -m 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -p -m 644 {config,*.action,default.filter,trust} %{buildroot}%{privoxyconf}/
install -p -m 644 templates/* %{buildroot}%{privoxyconf}/templates
install -p -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
# Upstream dropped this one:
#install -p -m 644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -m 711 -d %{buildroot}%{_localstatedir}/log/%{name}

# Customize the configuration file
sed -i -e 's@^confdir.*@confdir %{privoxyconf}@g' %{buildroot}%{privoxyconf}/config
sed -i -e 's@^logdir.*@logdir %{_localstatedir}/log/%{name}@g' %{buildroot}%{privoxyconf}/config

touch %{buildroot}%{_sysconfdir}/privoxy/user.filter

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
cp -p %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}


%pre
# Add user/group on install
if [ $1 -eq "1" ]; then
    %{_sbindir}/groupadd -g %{privoxy_gid} %{name} > /dev/null 2>&1 ||:
    %{_sbindir}/useradd -u %{privoxy_uid} -g %{privoxy_gid} -d %{privoxyconf} -r -s "/sbin/nologin" %{name} > /dev/null 2>&1 ||:
fi


%post
# Add privoxy service to  management facilities on install
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

if [[ ! -f %{_sysconfdir}/privoxy/user.filter ]]
then
    touch %{_sysconfdir}/privoxy/user.filter
fi

%preun
# Remove privoxy service from management facilities on erase
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable privoxy.service > /dev/null 2>&1 || :
    /bin/systemctl stop privoxy.service > /dev/null 2>&1 || :
fi

%postun
# Restart service if already running on upgrade
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart privoxy.service >/dev/null 2>&1 || :
fi

%clean
/bin/rm -rf %{buildroot}

%files
%defattr(-,%{name},%{name},-)
%dir %{_localstatedir}/log/%{name}

# Owned by root
%defattr(-,root,root,-)
#config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/privoxy/user.filter
%attr(0755,root,root)%{_sbindir}/%{name}
%config(noreplace) %{privoxyconf}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%doc README AUTHORS ChangeLog LICENSE 
%doc doc
#doc/source/developer-manual doc/source/faq doc/source/user-manual

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.0.23-3
- Rebuild

