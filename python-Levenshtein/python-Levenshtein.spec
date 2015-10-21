%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:         python-Levenshtein
Summary:      Python extension computing string distances and similarities
Version:      0.10.1
Release:      21%{?dist}

Group:        Development/Libraries
License:      GPLv2+

# The original site: http://trific.ath.cx/python/levenshtein/
# no longer exists so pointing to the pypi listing instead.
URL:          http://pypi.python.org/pypi/python-Levenshtein/

# The wayback machine provides this link to the original source:
# http://web.archive.org/web/20060715051500/http://trific.ath.cx/Ftp/python/levenshtein/python-Levenshtein-0.10.1.tar.bz2
# SHA1: d630141e003f47a43e0f8eacdcbf593bf9d15ed6
# The sourceforge files are a mirror of these files.
Source:       http://downloads.sourceforge.net/project/translate/%{name}/%{version}/%{name}-%{version}.tar.bz2

# The same applies to genextdoc.py see v 1.5:
# http://web.archive.org/web/20060717041205/http://trific.ath.cx/Ftp/python/genextdoc.py
# SHA1: 5c91974b102f42144529913ce181c1866451bcf6
Source1:      genextdoc.py
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python2-devel
BuildRequires: python-setuptools

%description
Levenshtein computes Levenshtein distances, similarity ratios, generalized
medians and set medians of Strings and Unicodes.  Because it's implemented
in C, it's much faster than corresponding Python library functions and
methods.


%prep
%setup -q
cp %{SOURCE1} .

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build
 
%install
rm -rf $RPM_BUILD_ROOT
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root $RPM_BUILD_ROOT
PYTHONPATH=$PYTHONPATH:$RPM_BUILD_ROOT/%{python_sitearch} %{__python} genextdoc.py Levenshtein

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING NEWS StringMatcher.py Levenshtein.html
%{python_sitearch}/*egg-info
%{python_sitearch}/Levenshtein.so

%changelog
* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.

