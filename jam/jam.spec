Name:		jam
Version:	2.5
Release:	18%{?dist}
License:	Copyright only
Summary:	Program construction tool, similar to make
URL:		http://public.perforce.com/public/jam/index.html
Source0:	ftp://ftp.perforce.com/jam/%{name}-%{version}.zip
# Submitted upstream by e-mail
Patch0:         jam-2.5-overflow.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	byacc

%description
Jam is a program construction tool, like make. Jam recursively builds target 
files from source files, using dependency information and updating actions 
expressed in the Jambase file, which is written in jam's own interpreted 
language. The default Jambase is compiled into jam and provides a boilerplate 
for common use, relying on a user-provide file "Jamfile" to enumerate actual 
targets and sources. 

%prep
%setup -q -c
%patch0 -p1 -b .overflows

%build
make CFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m0755 bin.linux*/jam $RPM_BUILD_ROOT/%{_bindir}
install -m0755 bin.linux*/mkjambase $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README RELNOTES *.html
%{_bindir}/jam
%{_bindir}/mkjambase

%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2.5-18
- Initial build

