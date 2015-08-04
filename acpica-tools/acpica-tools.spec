Name:           acpica-tools
Version:        20150619
Release:        5
Summary:        ACPICA tools for the development and debug of ACPI tables

Group:          Development/Languages
License:        GPLv2
URL:            https://www.acpica.org/

Source0:        https://acpica.org/sites/acpica/files/acpica-unix2-%{version}.tar.gz
Source1:        https://acpica.org/sites/acpica/files/acpitests-unix-%{version}.tar.gz
Source3:        iasl.1
Source4:        acpibin.1
Source5:        acpidump.1
Source6:        acpiexec.1
Source7:        acpihelp.1
Source8:        acpinames.1
Source9:        acpisrc.1
Source10:       acpixtract.1
Source11:       badcode.asl.result
Source12:       grammar.asl.result
Source13:       run-misc-tests.sh
Source14:       COPYING

BuildRequires:  bison flex

%description
The ACPI Component Architecture (ACPICA) project provides an OS-independent
reference implementation of the Advanced Configuration and Power Interface
Specification (ACPI).  ACPICA code contains those portions of ACPI meant to
be directly integrated into the host OS as a kernel-resident subsystem, and
a small set of tools to assist in developing and debugging ACPI tables.

This package contains only the user-space tools needed for ACPI table
development, not the kernel implementation of ACPI.  The following commands
are installed:
   -- iasl: compiles ASL (ACPI Source Language) into AML (ACPI Machine
      Language), suitable for inclusion as a DSDT in system firmware.
      It also can disassemble AML, for debugging purposes.
   -- acpibin: performs basic operations on binary AML files (e.g.,
      comparison, data extraction)
   -- acpidump: write out the current contents of ACPI tables
   -- acpiexec: simulate AML execution in order to debug method definitions
   -- acpihelp: display help messages describing ASL keywords and op-codes
   -- acpinames: display complete ACPI name space from input AML
   -- acpisrc: manipulate the ACPICA source tree and format source files
      for specific environments
   -- acpixtract: extract binary ACPI tables from acpidump output (see
      also the pmtools package)

This version of the tools is being released under GPLv2 license.

%prep
%setup -q -n acpica-unix2-%{version}
%setup -q -T -D -a 1 -n acpica-unix2-%{version}
gzip -dc %{SOURCE1} | tar -x --strip-components=1 -f -

cp -p %{SOURCE3} iasl.1
cp -p %{SOURCE4} acpibin.1
cp -p %{SOURCE5} acpidump.1
cp -p %{SOURCE6} acpiexec.1
cp -p %{SOURCE7} acpihelp.1
cp -p %{SOURCE8} acpinames.1
cp -p %{SOURCE9} acpisrc.1
cp -p %{SOURCE10} acpixtract.1
cp -p %{SOURCE11} badcode.asl.result
cp -p %{SOURCE12} grammar.asl.result
cp -p %{SOURCE13} tests/run-misc-tests.sh
chmod a+x tests/run-misc-tests.sh
cp -p %{SOURCE14} COPYING

# spurious executable permissions on text files in upstream
chmod a-x changes.txt
chmod a-x source/compiler/new_table.txt


%build
make OPT_CFLAGS="%{optflags}"

%install
# Install the binaries
mkdir -p %{buildroot}%{_bindir}
install -pD generate/unix/bin*/* %{buildroot}%{_bindir}/
mv %{buildroot}%{_bindir}/acpidump %{buildroot}%{_bindir}/acpidump-acpica
mv %{buildroot}%{_bindir}/acpixtract %{buildroot}%{_bindir}/acpixtract-acpica

# Install the man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -pDm 0644 -p -D *.1 %{buildroot}%{_mandir}/man1/
mv %{buildroot}%{_mandir}/man1/acpixtract.1 \
   %{buildroot}%{_mandir}/man1/acpixtract-acpica.1
mv %{buildroot}%{_mandir}/man1/acpidump.1 \
   %{buildroot}%{_mandir}/man1/acpidump-acpica.1

%check
#cd tests
#
## ASL tests
#./aslts.sh                         # relies on non-zero exit
#[ $? -eq 0 ] || exit 1
#
## API tests
#cd aapits
#make
#cd asl
#ASL=%{buildroot}%{_bindir}/iasl make
#cd ../bin
#./aapitsrun
#[ $? -eq 0 ] || exit 1
#cd ../..
#
## misc tests
#./run-misc-tests.sh %{buildroot}%{_bindir} %{version}
#
## Template tests
#cd templates
#make
#if [ -f diff.log ]
#then
#    if [ -s diff.log ]
#    then
#        exit 1                  # implies errors occurred
#    fi
#fi
#cd ..


%files
%doc changes.txt source/compiler/new_table.txt
%doc COPYING
%{_bindir}/*
%{_mandir}/*/*


%changelog
