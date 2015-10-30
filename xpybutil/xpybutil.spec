Name:		xpybutil
Version:	20141115
Release:	2
Summary:	A Python rendition of xcb-util. EWMH, ICCCM, key binding, Xinerama, etc...

License:    GPL	
URL:		http://burntsushi.net/X11/xpybutil
Source0:	xpybutil.tar.gz
BuildArch: noarch

BuildRequires: xpyb-devel

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n xpybutil

%build
%install
python ./setup.py install --root=$RPM_BUILD_ROOT
rm -rf %{buildroot}%{_docdir}
%files
%{python_sitearch}/xpybutil
%{python_sitearch}/*.egg-info

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 20141115-2
- Rebuild


