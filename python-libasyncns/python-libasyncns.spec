%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-libasyncns
Version:        0.7.1
Release:        13%{?dist}
Summary:        Python binding for libasyncns

License:        LGPLv2+
URL:            https://launchpad.net/libasyncns-python
Source0:        http://launchpad.net/libasyncns-python/trunk/%{version}/+download/libasyncns-python-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel libasyncns-devel >= 0.4

%description
Python binding for the libasyncns asynchronous name service query library.

%prep
%setup -q -n libasyncns-python-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{_libdir} -type f -exec chmod 0755 '{}' \;

%check
#make test

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README LICENSE
%{python_sitearch}/*


%changelog
* Thu Dec 03 2015 sulit <sulitsrc@gmail.com> - 0.7.1-13
- Init for isoft4

