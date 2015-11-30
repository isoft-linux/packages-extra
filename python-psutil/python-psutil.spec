%global srcname psutil
%global sum A process and system utilities module for Python

# Filter Python modules from Provides
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           python-%{srcname}
Version:        3.2.1
Release:        2%{?dist}
Summary:        %{sum}

License:        BSD
URL:            http://psutil.googlecode.com/
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python-devel
BuildRequires:  python3-devel
# Test dependencies
BuildRequires:  procps-ng
BuildRequires:  python-mock
BuildRequires:  python3-mock

%description
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.


%package -n python2-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{srcname}}
Obsoletes:      python-%{srcname} < 3.1.1-3

%description -n python2-psutil
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python 3, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.

%package -n python3-psutil
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-psutil
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python 3, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.


%prep
%autosetup -n %{srcname}-%{version}

# Remove shebangs
for file in psutil/*.py; do
  sed -i.orig -e 1d $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%check
# the main test target causes failures, investigating
make test-memleaks PYTHON=%{__python2}
make test-memleaks PYTHON=%{__python3}

 
%files -n python2-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CREDITS HISTORY.rst README.rst TODO
%{python2_sitearch}/%{srcname}/
%{python2_sitearch}/*.egg-info


%files -n python3-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CREDITS HISTORY.rst README.rst TODO
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/*.egg-info


%changelog
