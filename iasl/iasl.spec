Name:           iasl
Version:        20120913
Release:        9
Summary:        Intel ASL compiler/decompiler

Group:          Development/Languages
License:        Intel ACPI
URL:            https://www.acpica.org/
Source0:        http://www.acpica.org/download/acpica-unix-%{version}.tar.gz
Source1:        iasl-README.Fedora
Source2:	iasl.1
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  bison patchutils flex

# Configure.  See top of patch for details.
Patch0:         iasl-config.patch
Patch1:	        debian-big_endian.patch
Patch2:	        debian-unaligned.patch
Patch3:	        iasl-signed-char.patch

%description
iasl compiles ASL (ACPI Source Language) into AML (ACPI Machine Language),
which is suitable for inclusion as a DSDT in system firmware. It also can
disassemble AML, for debugging purposes.


%prep
%setup -q -n acpica-unix-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp -p %{SOURCE1} README.Fedora
cp -p %{SOURCE2} iasl.1

%build
# does not compile with %{?_smp_mflags}
make


%install
rm -rf $RPM_BUILD_ROOT
install -p -D generate/unix/bin*/iasl $RPM_BUILD_ROOT%{_bindir}/iasl
install -m 0644 -p -D iasl.1 $RPM_BUILD_ROOT%{_mandir}/man1/iasl.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc changes.txt README.Fedora
%{_bindir}/iasl
%{_mandir}/man1/iasl.1.gz


%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 20120913-9
- rebuilt for xen(libvirt)

