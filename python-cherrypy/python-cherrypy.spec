%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-cherrypy
Version:        3.5.0
Release:        2%{?dist}
Summary:        Pythonic, object-oriented web development framework
License:        BSD
URL:            http://www.cherrypy.org/
Source0:        http://download.cherrypy.org/cherrypy/%{version}/CherryPy-%{version}.tar.gz
# Don't ship the tests or tutorials in the python module directroy,
# tutorial will be shipped as doc instead
Patch0:         python-cherrypy-tutorial-doc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

%description
CherryPy allows developers to build web applications in much the same way 
they would build any other object-oriented Python program. This usually 
results in smaller source code developed in less time.

%prep
%setup -q -n CherryPy-%{version}
%patch0 -p1

%{__sed} -i 's/\r//' README.txt cherrypy/tutorial/README.txt cherrypy/tutorial/tutorial.conf

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
#cd cherrypy/test
## These two tests hang in the buildsystem so we have to disable them.
## The third fails in cherrypy 3.2.2.
#PYTHONPATH='../../' nosetests -s ./ -e 'test_SIGTERM' -e \
#  'test_SIGHUP_tty' -e 'test_file_stream'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.txt
%doc cherrypy/tutorial
%{_bindir}/cherryd
%{python_sitelib}/*

%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 3.5.0-2
- Initial build

