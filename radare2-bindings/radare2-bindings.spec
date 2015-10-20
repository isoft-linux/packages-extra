Name: radare2-bindings
Version: 0.9.9
Release: 1
Summary: radare2 language bindings for r2 api

License: GPLv3
URL: https://github.com/radare/radare2-bindings
Source0: http://rada.re/get/radare2-bindings-%{version}.tar.xz

BuildRequires: radare2-devel valabind	

%description
radare2 language bindings for r2 api

%package python
Summary: Python2 binding for radare2
Requires: radare2

%description python
Python2 binding for radare2

%package vala
Summary: Vala binding for radare2
Requires: vala
Requires: radare2

%description vala
Vala binding for radare2

%prep
%setup -q

%build
%configure --enable=python,ctypes,valac

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files python
%{python_sitearch}/r2
%{_libdir}/radare2/*/lang_duktape.so
%{_libdir}/radare2/*/lang_python.so

%files vala
%{_datadir}/vala/vapi/*
%changelog

