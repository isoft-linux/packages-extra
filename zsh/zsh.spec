Summary: Powerful interactive shell
Name: zsh
Version: 5.1.1
Release: 2%{?dist}
License: MIT
URL: http://zsh.sourceforge.net/
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: zshprompt.pl

#We package oh-my-zsh with zsh without seperate package for it,
#Since zsh will be better with oh-my-zsh.
#https://github.com/robbyrussell/oh-my-zsh
Source20: oh-my-zsh.tar.gz

# legacy downstream patches, TODO: either get them upstream or drop them
Patch0: zsh-serial.patch
Patch1: zsh-4.3.6-8bit-prompts.patch
Patch2: zsh-test-C02-dev_fd-mock.patch

# fix crash in ksh mode with -n and $HOME (#1269883)
Patch3: zsh-5.1.1-ksh-n-home.patch

BuildRequires: coreutils sed ncurses-devel libcap-devel
BuildRequires: texinfo gawk hostname
Requires(post): grep
Requires(postun): coreutils grep

Provides: /bin/zsh

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -p %SOURCE7 .

%build
# make loading of module's dependencies work again (#1277996)
export LIBLDFLAGS='-z lazy'

%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp --enable-maildir-support

make all html


%install
rm -rf $RPM_BUILD_ROOT

%makeinstall \
  fndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/functions \
  sitefndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/site-functions \
  scriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/scripts \
  runhelpdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -rf $RPM_BUILD_ROOT%{_infodir}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
    install -m 644 $i $RPM_BUILD_ROOT%{_sysconfdir}/"$(basename $i .rhs)"
done

#!!!! we do not provide zshrc with zsh, but provide it in rootfiles package, also, we use the one from oh-my-zsh
#We have to deal with a satuation that:
#'zsh not installed and user created, even user installed zsh, there is no chance to copy .zshrc for user.'

#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
#install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.zshrc

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
    chmod +x $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
done

sed -i "s!$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help!%{_datadir}/%{name}/%{version}/help!" \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/{run-help,_run-help}


#for oh-my-zsh
tar zxf %{SOURCE20} -C %{buildroot}%{_datadir}/zsh
rm -rf %{buildroot}%{_datadir}/zsh/oh-my-zsh/.git*

%clean
rm -rf $RPM_BUILD_ROOT


%check
# Run the testsuite
make check

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/%{name}" > %{_sysconfdir}/shells
    echo "/bin/%{name}" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    grep -q "^/bin/%{name}$" %{_sysconfdir}/shells || echo "/bin/%{name}" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/%{name}$!d' %{_sysconfdir}/shells
fi


%files
%defattr(-,root,root)
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide zshprompt.pl
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_datadir}/zsh
%{_libdir}/zsh
#%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 5.1.1-2
- Initial build
- Package oh-my-zsh with this package.

