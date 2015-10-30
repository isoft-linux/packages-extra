%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global SVN 362

Name:           uniconvertor
Version:        2.0
Release:        0.9%{?SVN:.svn%{SVN}}%{?dist}
Summary:        Universal vector graphics translator

License:        LGPLv2+ and GPLv2+ and MIT
URL:            http://sk1project.org/modules.php?name=Products&product=uniconvertor
# Script to reproduce given tarball from source0
Source1:        %{name}.get.tarball.svn
Source0:        %{name}-%{version}svn%{SVN}.tar.xz

BuildRequires:  python-devel, pycairo-devel, python-pillow-devel, lcms2-devel
BuildRequires:  potrace-devel
# For a public domain sRGB.icm
BuildRequires:  argyllcms
Requires:       python-imaging, python-reportlab, python-pillow, pycairo


%description
UniConvertor is a universal vector graphics translator.
It uses sK1 engine to convert one format to another.

%prep
%setup -q
cp -a /usr/share/color/argyll/ref/sRGB.icm src/unittests/cms_tests/cms_data/sRGB.icm

%build
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/python2.7/Imaging" python setup.py build

%install
python setup.py install --skip-build --root %{buildroot}

%post
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
update-mime-database -n %{_datadir}/mime &> /dev/null || :

%files
%doc README LICENSE GPLv3.txt
%{_bindir}/%{name}
%{python_sitearch}/*
%{_datarootdir}/mime-info/sk1project.keys
%{_datarootdir}/mime-info/sk1project.mime
%{_datarootdir}/mime/packages/vnd.sk1project.pdxf-graphics.xml

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0-0.9.svn362
- Rebuild

* Wed Oct 21 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
