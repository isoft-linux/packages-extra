# Fedora spec file for php-pecl-jsonc
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

%global pecl_name  json
%global proj_name  jsonc
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:       Support for JSON serialization
Name:          php-pecl-%{proj_name}
Version:       1.3.9
Release:       2%{?dist}
# PHP extension is PHP
# jsonc-c is MIT
# json-c/linkhask.c is Public Domain
License:       PHP and MIT and Public Domain
URL:           http://pecl.php.net/package/%{proj_name}
Source0:       http://pecl.php.net/get/%{proj_name}-%{version}%{?prever}.tgz

BuildRequires: php-devel >= 5.4
BuildRequires: php-pear
BuildRequires: pcre-devel

Provides:      bundled(libjson-c) = 0.11
Provides:      bundled(bobjenkins-hash)

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:      php-pecl(%{proj_name}) = %{version}
Provides:      php-pecl(%{proj_name})%{?_isa} = %{version}


%description
The %{name} module will add support for JSON (JavaScript Object Notation)
serialization to PHP.

This is a dropin alternative to standard PHP JSON extension which
use the json-c library parser.


%package devel
Summary:       JSON developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using JSON serializer.


%prep
%setup -q -c 
cd %{proj_name}-%{version}%{?prever}

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_JSON_VERSION/{s/.* "//;s/".*$//;p}' php_json.h )
if test "x${extver}" != "x%{version}%{?prever:%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:%{prever}}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF

# duplicate for ZTS build
cp -pr %{proj_name}-%{version}%{?prever} %{proj_name}-zts


%build
cd %{proj_name}-%{version}%{?prever}
%{_bindir}/phpize
%configure \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{proj_name}-zts
%{_bindir}/zts-phpize
%configure \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C %{proj_name}-%{version}%{?prever} \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
make -C %{proj_name}-zts \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{proj_name}-%{version}%{?prever}/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{proj_name}-%{version}%{?prever}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{proj_name}-%{version}%{?prever}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

cd ../%{proj_name}-zts

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php


# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi


%files
%{?_licensedir:%license %{proj_name}-%{version}%{?prever}/LICENSE}
%{?_licensedir:%license %{proj_name}-%{version}%{?prever}/json-c/COPYING}
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%files devel
%{php_incldir}/ext/json
%{php_ztsincldir}/ext/json
%doc %{pecl_testdir}/%{pecl_name}


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 1.3.9-2
- Initial build

