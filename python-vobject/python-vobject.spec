%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-vobject 
Version:        0.8.1c 
Release:        12%{?dist}
Summary:        A python library for manipulating vCard and vCalendar files

Group:          Development/Languages
License:        ASL 2.0
URL:            http://vobject.skyhouseconsulting.com/ 
Source0:        http://vobject.skyhouseconsulting.com/vobject-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-dateutil15
Requires:       python-setuptools

Patch1:         no-ez-setup.patch
Patch2:         0001-Require-dateutil-1.5.patch

%description
VObject is intended to be a full featured python library for parsing and
generating vCard and vCalendar files.


%prep
%setup -q -n vobject-%{version}
%patch1 -p1
%patch2 -p1


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ACKNOWLEDGEMENTS.txt LICENSE-2.0.txt README.txt

%{python_sitelib}/*

%{_bindir}/change_tz
%{_bindir}/ics_diff


%changelog
* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.

