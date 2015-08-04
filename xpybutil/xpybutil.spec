Name:		xpybutil
Version:	20141115
Release:	1
Summary:	A Python rendition of xcb-util. EWMH, ICCCM, key binding, Xinerama, etc...

Group:		GUI/Runtime/Library
License:    GPL	
URL:		http://burntsushi.net/X11/xpybutil
Source0:	xpybutil.tar.gz
BuildRequires: xpyb-devel

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
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

