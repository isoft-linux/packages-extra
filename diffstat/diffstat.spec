Summary: A utility which provides statistics based on the output of diff
Name: diffstat
Version: 1.60
Release: 2
License: MIT
URL: http://invisible-island.net/diffstat
Source0: ftp://invisible-island.net/diffstat/%{name}-%{version}.tgz
# Taken from diffstat.c.
Source1: COPYING
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: xz

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

Install diffstat if you need a program which provides a summary of the
diff command's output.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
cp %{SOURCE1} .

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING CHANGES README
%{_bindir}/diffstat
%{_mandir}/*/*

%changelog
* Fri Nov 27 2015 xiaotian.wu@i-soft.com.cn - 1.60-2
- rebuilt

* Fri Nov 27 2015 xiaotian.wu@i-soft.com.cn - 1.60-2
- init for isoft

