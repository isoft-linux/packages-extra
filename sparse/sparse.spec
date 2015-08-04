Name:		sparse
Version:    git20150624	
Release:	1
Summary:	C semantic parser

Group:	    Extra/Runtime/Lirary	
License:	MIT
URL:		https://git.kernel.org/cgit/devel/sparse/sparse.git/
Source0:	%{name}.tar.gz
Patch0:     sparse-disable-one-test-clang-not-support.patch

%description
Sparse is a semantic parser of source files: it's neither a compiler
(although it could be used as a front-end for one) nor is it a
preprocessor (although it contains as a part of it a preprocessing
phase). 


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1
sed -i "s@-finline-functions@@g" Makefile

%build
make %{?_smp_mflags} CC=clang LD=clang

%install
make install DESTDIR=%{buildroot} PREFIX=/usr

sed -i "s@gcc@clang@g" $RPM_BUILD_ROOT%{_bindir}/sparsec
rpmclean

%files
%{_bindir}/c2xml
%{_bindir}/cgcc
%{_bindir}/sparse
%{_bindir}/sparse-llvm
%{_bindir}/sparsec
%{_bindir}/test-inspect
%{_mandir}/man1/cgcc.1.gz
%{_mandir}/man1/sparse.1.gz

%files devel
%dir %{_includedir}/sparse
%{_includedir}/sparse/*
%{_libdir}/libsparse.a
%{_libdir}/pkgconfig/sparse.pc

%changelog

