%global with_python3 1
%global real_version %(eval echo %{pkg_version} | %{__sed} 's/-/./')


%filter_provides_in %{python_sitearch}/.*\.so$ 
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$ 
%endif # if with_python3
%filter_setup

Name:               python-apsw
Version:            3.8.11.1 
Release:            4%{?dist}
Summary:            Another Python SQLite Wrapper
License:            zlib
URL:                http://code.google.com/p/apsw/
Source:             https://github.com/rogerbinns/apsw/releases/download/%{version}-r1/apsw-%{version}-r1.zip

Requires:           sqlite

BuildRequires:      sqlite-devel
BuildRequires:      python2-devel
%if 0%{?with_python3}
BuildRequires:      python3-devel
%endif # if with_python3



%description
APSW is a Python wrapper for the SQLite embedded relational database
engine. In contrast to other wrappers such as pysqlite it focuses on
being a minimal layer over SQLite attempting just to translate the
complete SQLite API into Python.
%if 0%{?with_python3}
%package -n python3-apsw
Summary:            Another Python SQLite Wrapper Python 3 packages

%description -n python3-apsw
APSW is a Python 3 wrapper for the SQLite embedded relational database
engine. In contrast to other wrappers such as pysqlite it focuses on
being a minimal layer over SQLite attempting just to translate the
complete SQLite API into Python 3.
%endif # with_python3



%prep
%setup -q -n apsw-%{version}-r1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build

CFLAGS="$RPM_OPT_FLAGS" python2 setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" python3 setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
python3 setup.py install --root %{buildroot}
popd
%endif # with_python3

python2 setup.py install --root %{buildroot}

%files
%doc doc/*
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-apsw
%doc doc/*
%{python3_sitearch}/*
%endif # with_python3

%changelog
* Fri Nov 06 2015 Cjacker <cjacker@foxmail.com> - 3.8.11.1-4
- Rebuild with python 3.5

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - %{pkg_version}-3
- Initial build

