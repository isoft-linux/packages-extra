Name:		valkyrie
Version:	2.0.1
Release:	2.svn20150713
Summary:	A Qt based GUI for valgrind

License:    GPL	
URL:		http://valgrind.org/downloads/guis.html
Source0:	valkyrie.tar.xz
Patch0:     valkyrie-build-fix.patch
BuildRequires: qt4-devel	
Requires:	qt4, valgrind

%description
Valkyrie is a Qt-based GUI for the Memcheck and Helgrind tools of Valgrind 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
qmake-qt4 PREFIX=/usr DOCDIR=/usr/share/doc
make %{?_smp_mflags}


%install

make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}


%files
/

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2.0.1-2.svn20150713
- Rebuild


