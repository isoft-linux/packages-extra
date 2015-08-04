%global       releasedate 20120801
%global       release_date %{lua:reldate=rpm.expand("%{releasedate}");print(("%s-%s-%s"):format(reldate:sub(0,4),reldate:sub(5,6),reldate:sub(7)))}

Name:         ksh
Summary:      The Original ATT Korn Shell
URL:          http://www.kornshell.com/
Group:        System Environment/Shells
#zlib is used for INIT.2010-02-02.tgz/src/cmd/INIT/ratz.c - used only for build tool
#CPL everywhere else (for KSH itself)
License:      CPL
Version:      %{releasedate}
Release:      24%{?dist}
Source0:      http://www.research.att.com/~gsf/download/tgz/ast-ksh.%{release_date}.tgz
Source1:      http://www.research.att.com/~gsf/download/tgz/INIT.%{release_date}.tgz
Source2:      kshcomp.conf
Source3:      kshrc.rhs
Source4:      dotkshrc

# expected results of test suite
Source5:      expectedresults.log

# don't use not wanted/needed builtins - Fedora/RHEL specific
Patch1:       ksh-20070328-builtins.patch

# fix regression test suite to be usable during packagebuild - Fedora/RHEL specific
Patch2:      ksh-20100826-fixregr.patch

# fedora/rhel specific, rhbz#619692
Patch6:       ksh-20080202-manfix.patch

# rhbz#702008
Patch17:      ksh-20100202-pathvar.patch

# rhbz#924440
Patch18:      ksh-20100621-fdstatus.patch

# fixes for regressions found in ksh-20120801 rebase
Patch19:      ksh-20120801-rmdirfix.patch
Patch20:      ksh-20120801-cdfix.patch
Patch21:      ksh-20120801-cdfix2.patch
Patch22:      ksh-20120801-tabfix.patch
Patch23:      ksh-20130214-fixkill.patch

# for ksh <= 2013-05-31, rhbz#960034
Patch24:      ksh-20120801-kshmfix.patch

# for ksh <= 2016-06-28, rhbz#921455
Patch25:      ksh-20120801-memlik.patch

# for ksh <= 2013-03-20, rhbz#922851
Patch26:      ksh-20120801-forkbomb.patch

# for ksh <= 2013-04-19, rhbz#913110
Patch27:      ksh-20120801-macro.patch

# not completely upstream yet, rhbz#858263
Patch29:      ksh-20130628-longer.patch

# for ksh <= 2013-07-19, rhbz#982142
Patch30: ksh-20120801-mlikfiks.patch

# not yet upstream, related to 2012-08-01 rebase
Patch31: ksh-20120801-covsfix.patch

# rhbz#1007816
Patch32: ksh-20100621-manfix3.patch

# rhbz#1016611
Patch33: ksh-20120801-nomulti.patch

# from upstream, rhbz#1036802
Patch34: ksh-20120801-fd2lost.patch

# for ksh <= 2014-01-14, rhbz#1036470
Patch35: ksh-20120801-memlik3.patch

# for ksh <= 2014-03-04, rhbz#1066589
Patch36: ksh-20120801-filecomsubst.patch

# for ksh <= 2014-04-05, rhbz#825520
Patch37: ksh-20120801-crash.patch

# for ksh < 2013-03-19, rhbz#1075635
Patch38: ksh-20120801-sufix.patch

# for ksh < 2014-03, rhbz#1047506
Patch39: ksh-20120801-argvfix.patch

# sent upstream, rhbz#1078698
Patch40: ksh-20140301-fikspand.patch

# for ksh < 2014-04-15, rhbz#1070350
Patch41: ksh-20120801-roundit.patch

# for ksh < 2014-04-15, rhbz#1036931
Patch42: ksh-20120801-heresub.patch

# not included upstream yet, rhbz#1062296
Patch43: ksh-20140415-hokaido.patch

# for ksh < 20121004, rhbz#1083713
Patch44: ksh-20120801-tpstl.patch

# for ksh <= 20120214, rhbz#1023109
Patch45: ksh-20120801-mtty.patch

# sent upstream, rhbz#1019334
Patch46: ksh-20120801-manfix4.patch

# not upstream yet, rhbz#1105138
Patch47: ksh-20120801-fununset.patch

# not upstream yet, rhbz#1102627
Patch48: ksh-20120801-cdfix3.patch

# sent upstream, rhbz#1112306
Patch49: ksh-20120801-locking.patch

# for ksh <= 2013-06-13, rhbz#1133582
Patch50: ksh-20130613-cdfix4.patch
Patch51: ksh-20120801-retfix.patch

# not upstream yet, rhbz#1147645
Patch52: ksh-20120801-oldenvinit.patch

# not upstream yet, rhbz#1160923
Patch53: ksh-20120801-noexeccdfix.patch

# sent upstream, for ksh <= 2014-09-30, rhbz#1168611
Patch54: ksh-20120801-cdfork.patch

# from upsteam, for ksh < 2012-10-04, rhbz#1173668
Patch55: ksh-20120801-emptyarrayinit.patch

# not upstream yet, rhbz#1188377
Patch56: ksh-20120801-xufix.patch

# sent upstream, for ksh <= 2015-02-10, rhbz#1189294
Patch57: ksh-20120801-assoc-unset-leak.patch

# sent upstream, for ksh <= 2014-12-18, rhbz#1176670
Patch58: ksh-20120801-alarmifs.patch

# not yet upstream, rhbz#1116072
Patch59: ksh-20140929-safefd.patch

# workaround, for ksh < 2013-05-24, rhbz#1117404
Patch60: ksh-20120801-trapcom.patch

# for ksh <= 2013-04-09, rhbz#960371
Patch61: ksh-20120801-lexfix.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:    pdksh
Requires: coreutils, glibc-common, diffutils
BuildRequires: bison
# regression test suite uses 'ps' from procps
BuildRequires: procps
Requires(post): grep, coreutils, systemd-units
Requires(preun): grep, coreutils

%description
KSH-93 is the most recent version of the KornShell by David Korn of
AT&T Bell Laboratories.
KornShell is a shell programming language, which is upward compatible
with "sh" (the Bourne Shell).

%prep
%setup -q -c
%setup -q -T -D -a 1
%patch1 -p1 -b .builtins
%patch2 -p1 -b .fixregr
%patch6 -p1 -b .manfix
%patch17 -p1 -b .pathvar
%patch18 -p1 -b .fdstatus
%patch19 -p1 -b .rmdirfix
%patch20 -p1 -b .cdfix
%patch21 -p1 -b .cdfix2
%patch22 -p1 -b .tabfix
%patch23 -p1 -b .fixkill
%patch24 -p1 -b .kshmfix
%patch25 -p1 -b .memlik
%patch26 -p1 -b .forkbomb
%patch27 -p1 -b .macro
%patch29 -p1 -b .longer
%patch30 -p1 -b .mlikfiks
%patch31 -p1 -b .covsfix
%patch32 -p1 -b .manfix3
%patch33 -p1 -b .nomulti
%patch34 -p1 -b .fd2lost
%patch35 -p1 -b .memlik3
%patch36 -p1 -b .filecomsubst
%patch37 -p1 -b .crash
%patch38 -p1 -b .sufix
%patch39 -p1 -b .argvfix
%patch40 -p1 -b .fikspand
%patch41 -p1 -b .roundit
%patch42 -p1 -b .heresub
%patch43 -p1 -b .hokaido
%patch44 -p1 -b .tpstl
%patch45 -p1 -b .mtty
%patch46 -p1 -b .manfix4
%patch47 -p1 -b .fununset
%patch48 -p1 -b .cdfix3
%patch49 -p1 -b .locking
%patch50 -p1 -b .cdfix4
%patch51 -p1 -b .retfix
%patch52 -p1 -b .oldenvinit
%patch53 -p1 -b .noexeccdfix
%patch54 -p1 -b .cdfork
%patch55 -p1 -b .emptyarrayinit
%patch56 -p1 -b .xufix
%patch57 -p1 -b .assoc-unset-leak
%patch58 -p1 -b .alarmifs
%patch59 -p1 -b .safefd
%patch60 -p1 -b .trapcom
%patch61 -p1 -b .lexfix

#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

# sh/main.c was not using CCFLAGS
sed -i '/-c sh\/main.c/s|${mam_cc_FLAGS} |${mam_cc_FLAGS} ${CCFLAGS} |p' src/cmd/ksh93/Mamfile

# disable register for debugging
sed -i 1i"#define register" src/lib/libast/include/ast.h

%build
XTRAFLAGS=""
for f in -Wno-unknown-pragmas -Wno-missing-braces -Wno-unused-result -Wno-return-type -Wno-int-to-pointer-cast -Wno-parentheses -Wno-unused -Wno-unused-but-set-variable -Wno-cpp -P
do
  gcc $f -E - </dev/null >/dev/null 2>&1 && XTRAFLAGS="$XTRAFLAGS $f"
done
./bin/package
./bin/package make mamake ||:
./bin/package make mamake ||:
export CCFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing $XTRAFLAGS"
export CC=gcc
./bin/package make -S

#cp lib/package/LICENSES/epl LICENSE

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,%{_bindir},%{_mandir}/man1}
install -c -m 755 arch/*/bin/ksh $RPM_BUILD_ROOT/bin/ksh
install -c -m 755 arch/*/bin/shcomp $RPM_BUILD_ROOT%{_bindir}/shcomp
install -c -m 644 arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ksh.1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.kshrc
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/kshrc
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/binfmt.d/kshcomp.conf

%check
[ -f ./skipcheck -o -f ./../skipcheck ] && exit 0 ||:
%if 0%{?rhel} > 6
%ifarch s390
exit 0
%endif
%endif

export SHELL=$(ls $(pwd)/arch/*/bin/ksh)
cd src/cmd/ksh93/tests/
ulimit -c unlimited
if [ ! -e /dev/fd ]
then
  echo "ERROR: /dev/fd does not exist, regression tests skipped"
  exit 0
fi
$SHELL ./shtests 2>&1 | tee testresults.log
ls core.* 2>/dev/null ||:
exit 0
sed -e '/begins at/d' -e '/ 0 error/d' -e 's/at [^\[]*\[/\[/' testresults.log -e '/tests skipped/d' >filteredresults.log
if ! cmp filteredresults.log %{SOURCE5} >/dev/null || ls core.*
then
  echo "Regression tests failed"
  diff -Naurp %{SOURCE5} filteredresults.log
  exit -1
fi

%post
if [ ! -f /etc/shells ]; then
        echo "/bin/ksh" > /etc/shells
else
        if ! grep -q '^/bin/ksh$' /etc/shells ; then
                echo "/bin/ksh" >> /etc/shells
        fi
fi

/bin/systemctl try-restart systemd-binfmt.service >/dev/null 2>&1 || :

%postun
if [ ! -f /bin/ksh ]; then
    sed -i '/^\/bin\/ksh$/ d' /etc/shells
fi

%verifyscript
echo -n "Looking for ksh in /etc/shells... "
if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from /etc/shells" >&2
else
    echo "found"
fi

%files 
%defattr(-, root, root,-)
%doc src/cmd/ksh93/COMPATIBILITY src/cmd/ksh93/RELEASE src/cmd/ksh93/TYPES 
# LICENSE file is missing, temporarily?
/bin/ksh
/usr/bin/shcomp
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/skel/.kshrc
%config(noreplace) %{_sysconfdir}/kshrc
%config(noreplace) %{_sysconfdir}/binfmt.d/kshcomp.conf

%clean
    rm -rf $RPM_BUILD_ROOT

%changelog
