Summary: An enhanced version of csh, the C shell
Name: tcsh
Version: 6.19.00
Release: 1%{?dist}
License: BSD
Source: ftp://ftp.astron.com/pub/tcsh/tcsh-%{version}.tar.gz
Patch0: 0001-avoid-gcc-5-optimization-malloc-memset-calloc-Fridol.patch
Patch1: 0002-make-k-volatile-to-prevent-gcc-5-memset-optimization.patch

Provides: csh = %{version}
Provides: /bin/tcsh, /bin/csh
Requires(post): grep
Requires(postun): coreutils, grep

URL: http://www.tcsh.org/

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, ncurses-devel, gettext-devel, git


%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.


%prep
%autosetup -p1


%build
%configure --without-hesiod
make %{?_smp_mflags} all


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}
install -p -m 755 tcsh ${RPM_BUILD_ROOT}%{_bindir}/tcsh
install -p -m 644 tcsh.man ${RPM_BUILD_ROOT}%{_mandir}/man1/tcsh.1
ln -sf tcsh ${RPM_BUILD_ROOT}%{_bindir}/csh
ln -sf tcsh.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/csh.1

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ ! -f /etc/shells ]; then
 echo "%{_bindir}/tcsh" >> /etc/shells
 echo "%{_bindir}/csh"	>> /etc/shells
else
 grep -q '^%{_bindir}/tcsh$' /etc/shells || \
 echo "%{_bindir}/tcsh" >> /etc/shells
 grep -q '^%{_bindir}/csh$'  /etc/shells || \
 echo "%{_bindir}/csh"	>> /etc/shells
fi


%postun
if [ ! -x %{_bindir}/tcsh ]; then
 grep -v '^%{_bindir}/tcsh$'  /etc/shells | \
 grep -v '^%{_bindir}/csh$' > /etc/shells.rpm && \
 mv /etc/shells.rpm /etc/shells
fi


%files
%defattr(-,root,root,-)
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 6.18.01-14
- Initial build

