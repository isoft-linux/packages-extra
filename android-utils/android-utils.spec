Name: android-utils 
Version: 4.1.2
Release: 2
Summary: Standalone version of adb/aapt/zipalign/aidl/acp from Android

License: Refer to android  
URL: https://github.com/cjacker/android-utils
Source0: %{name}.tar.xz

BuildRequires: zlib-devel libpng-devel
BuildRequires: autoconf automake libtool

%description
%{summary}

%prep
%setup -q -n %{name}

%build
./autogen.sh
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/*

%changelog
* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 4.1.2-2
- Initial build


