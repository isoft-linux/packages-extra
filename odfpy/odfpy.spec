%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		odfpy
Version:	0.9.6
Release:	4%{?dist}
Summary:	Python library for manipulating OpenDocument files

License:	GPLv2+
URL:		https://joinup.ec.europa.eu/software/odfpy/home
# This changes every time, most recent downloads are at http://forge.osor.eu/frs/?group_id=33
Source0:	https://pypi.python.org/packages/source/o/odfpy/odfpy-0.9.6.tar.gz

BuildArch:	noarch
BuildRequires:	python-devel python-setuptools

%description
Odfpy aims to be a complete API for OpenDocument in Python. Unlike
other more convenient APIs, this one is essentially an abstraction
layer just above the XML format. The main focus has been to prevent
the programmer from creating invalid documents. It has checks that
raise an exception if the programmer adds an invalid element, adds an
attribute unknown to the grammar, forgets to add a required attribute
or adds text to an element that doesn't allow it.
 
These checks and the API itself were generated from the RelaxNG
schema, and then hand-edited. Therefore the API is complete and can
handle all ODF constructions, but could be improved in its
understanding of data types.


%prep
%setup -q


%build
CFLAGS="%{optflags}" python -c 'import setuptools; execfile("setup.py")' build


%install
python -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}
sed -i '/#!\/usr\/bin\/python/d' %{buildroot}%{python_sitelib}/odf/*.py

 
%files
%doc examples contrib
%{_bindir}/*
%{_mandir}/man1/*
%{python_sitelib}/*egg-info
%{python_sitelib}/odf


%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 0.9.6-4
- Initial build

