%global with_python3 1
%global tarname empy

Name:           python-empy
Version:        3.3.2
Release:        7%{?dist}
Summary:        A powerful and robust template system for Python
License:        LGPLv2+
URL:            http://www.alcyone.com/software/empy/
Source:         http://www.alcyone.com/software/%{tarname}/%{tarname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python-setuptools
%endif # if with_python3

%description
EmPy is a system for embedding Python expressions and statements in template
text; it takes an EmPy source file, processes it, and produces output. 

%if 0%{?with_python3}
%package -n python3-empy
Summary:        A powerful and robust template system for Python

%description -n python3-empy
EmPy is a system for embedding Python expressions and statements in template
text; it takes an EmPy source file, processes it, and produces output. 
%endif # with_python3

%prep
%setup -q -n %{tarname}-%{version}

#fix shebang on rpmlint
sed -i -e '1d' em.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
%endif # with_python3

%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc COPYING README version.txt
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-empy
%doc COPYING README version.txt
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.3.2-7
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 3.3.2-6
- Initial build

