%global with_python3 1 
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:           pyparsing
Version:        1.5.6
Release:        6
Summary:        An object-oriented approach to text processing
License:        MIT
URL:            http://pyparsing.wikispaces.com/
Source0:        http://downloads.sourceforge.net/pyparsing/pyparsing-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3

%description
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

%package doc
Summary:        Documentation for pyparsing

%description doc
The package contains documentation for pyparsing.

%if 0%{?with_python3}
%package -n python3-pyparsing
Summary:        An object-oriented approach to text processing (Python 3 version)

%description -n python3-pyparsing
pyparsing is a module that can be used to easily and directly configure syntax
definitions for any number of text parsing applications.

This is the Python 3 version.
%endif # if with_python3

%prep
%setup -q
mv docs/pyparsingClassDiagram.PNG docs/pyparsingClassDiagram.png
rm docs/pyparsingClassDiagram.JPG

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

# Install python 3 first, so that python 2 gets precedence:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES README LICENSE
%{python_sitelib}/pyparsing*egg-info
%{python_sitelib}/pyparsing.py*

%if 0%{?with_python3}
%files -n python3-pyparsing
%defattr(-,root,root,-)
%doc CHANGES README LICENSE
%{python3_sitelib}/pyparsing*egg-info
%{python3_sitelib}/pyparsing.py*
%endif # with_python3
%if 0%{?with_python3}
%{python3_sitelib}/__pycache__/pyparsing*
%endif # pycache

%files doc
%defattr(-,root,root,-)
%doc CHANGES README LICENSE docs/*

%changelog
