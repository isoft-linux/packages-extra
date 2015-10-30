%ifarch %{arm} %{ix86} x86_64 
%global __with_hipe 1
%endif

%define _javadir %{_datadir}/java

Name: erlang
Version: 18.1
Release: 2
Summary: Erlang programing language

License: Apache License 2.0
URL: http://www.erlang.org
Source0: http://www.erlang.org/download/otp_src_%{version}.tar.gz

Source5: epmd.service
Source6: epmd.socket
Source7: epmd@.service
Source8: epmd@.socket

Source10: erlang-init.el

BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	flex
BuildRequires:	m4
BuildRequires:  openjdk
BuildRequires:  wxGTK28-devel

%description
Erlang is a programming language used to build massively scalable soft real-time systems with requirements on high availability. Some of its uses are in telecoms, banking, e-commerce, computer telephony and instant messaging. Erlang's runtime system has built-in support for concurrency, distribution and fault tolerance.

%prep
%setup -q -n otp_src_%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %configure \
	--enable-shared-zlib \
	--enable-sctp \
	--enable-systemd \
	%{?__with_hipe:--enable-hipe}

# Remove pre-built BEAM files
make clean
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# GNU Emacs related stuff
erlang_tools_vsn="$(sed -n 's/TOOLS_VSN = //p' lib/tools/vsn.mk)"

# GNU Emacs related stuff
install -m 0755 -d "$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/"
install -m 0755 -d "$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/erlang"
install -m 0644 %{SOURCE10} "$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/erlang-init.el"
for f in %{buildroot}%{_libdir}/erlang/lib/tools-${erlang_tools_vsn}/emacs/{README,*.el}; do
        b="$(basename "$f")";
        ln -s "%{_libdir}/erlang/lib/tools-${erlang_tools_vsn}/emacs/$b" \
                "$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/erlang/"
done


# symlink *.jar files to appropriate places for subpackages
install -m 0755 -d "$RPM_BUILD_ROOT%{_javadir}/%{name}"

# erlang-ic
ic_lib_dir="$(ls -d1 $RPM_BUILD_ROOT%{_libdir}/erlang/lib/ic-*/ | sed "s,^$RPM_BUILD_ROOT,,")"
test -d "$RPM_BUILD_ROOT$ic_lib_dir"
ln -s "${ic_lib_dir}/priv/ic.jar" "$RPM_BUILD_ROOT%{_javadir}/%{name}/"

# erlang-jinterface
jinterface_lib_dir="$(ls -d1 $RPM_BUILD_ROOT%{_libdir}/erlang/lib/jinterface-*/ | sed "s,^$RPM_BUILD_ROOT,,")"
test -d "$RPM_BUILD_ROOT$jinterface_lib_dir"
install -m 0755 -d "$RPM_BUILD_ROOT%{_javadir}"
ln -s "${jinterface_lib_dir}priv/OtpErlang.jar" "$RPM_BUILD_ROOT%{_javadir}/%{name}/"


# Win32-specific man-pages
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man1/erlsrv.*
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man1/werl.*
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man3/win32reg.*

# remove empty directory
rm -r $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/man

# remove outdated script
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/Install

# systemd-related stuff
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/epmd.service
install -D -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/epmd.socket
install -D -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/epmd@.service
install -D -p -m 0644 %{SOURCE8} %{buildroot}%{_unitdir}/epmd@.socket


%files
%{_bindir}/*
%dir %{_libdir}/erlang
%{_libdir}/erlang/*
%{_datadir}/java/%{name}
%{_datadir}/emacs/site-lisp/site-start.d/erlang-init.el
%{_datadir}/emacs/site-lisp/erlang/
%{_unitdir}/epmd*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 18.1-2
- Rebuild

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- initial build.
