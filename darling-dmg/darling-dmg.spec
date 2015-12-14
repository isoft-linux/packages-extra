Name: darling-dmg 
Version: 0.1 
Release: 2
Summary: Allow ordinary users to directly mount OS X disk images under Linux via FUSE. 

License: GPL
URL: https://github.com/tpoechtrager/darling-dmg
Source0: %{name}.tar.xz

BuildRequires: libicu-devel openssl-devel zlib-devel bzip2-devel fuse-devel

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}

%build
mkdir -p %{_target_platform}

pushd %{_target_platform}
%cmake \
    ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install DESTDIR=%{buildroot} -C %{_target_platform}

%files
%{_bindir}/darling-dmg

%changelog
* Sun Dec 13 2015 Cjacker <cjacker@foxmail.com> - 0.1-2
- Initial build


