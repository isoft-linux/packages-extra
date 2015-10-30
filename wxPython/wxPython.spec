%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define buildflags WX_CONFIG=/usr/lib/wx/config/gtk2-unicode-3.0 WXPORT=gtk2 UNICODE=1

Name:           wxPython
Version:        3.0.1.1
Release:        2 

Summary:        GUI toolkit for the Python programming language

License:        LGPL
URL:            http://www.wxpython.org/
Source0:        http://dl.sf.net/wxpython/wxPython-src-%{version}.tar.bz2
BuildRequires:  wxWidgets-gtk2-shared-devel >= 3.0.0
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel, libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  libGL-devel, libGLU-devel
BuildRequires:  python-devel

# packages should depend on "wxPython", not "wxPythonGTK2", but in case
# one does, here's the provides for it.
Provides:       wxPythonGTK2 = %{version}-%{release}

%description
wxPython is a GUI toolkit for the Python programming language. It allows
Python programmers to create programs with a robust, highly functional
graphical user interface, simply and easily. It is implemented as a Python
extension module (native code) that wraps the popular wxWindows cross
platform GUI library, which is written in C++.

%package        devel
Summary:        Development files for wxPython add-on modules
Requires:       %{name} = %{version}-%{release}

%description devel
This package includes C++ header files and SWIG files needed for developing
add-on modules for wxPython. It is NOT needed for development of most
programs which use the wxPython toolkit.


%prep
%setup -q -n wxPython-src-%{version}

%build
export CC=clang++
export CXX=clang++

# Just build the wxPython part
cd wxPython
# included distutils is not multilib aware; use normal
rm -rf distutils
python setup.py %{buildflags} build


%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
python setup.py %{buildflags} install --root=$RPM_BUILD_ROOT

# this is a kludge....
%if "%{python_sitelib}" != "%{python_sitearch}"
mv $RPM_BUILD_ROOT%{python_sitelib}/wx.pth  $RPM_BUILD_ROOT%{python_sitearch}
mv $RPM_BUILD_ROOT%{python_sitelib}/wxversion.py* $RPM_BUILD_ROOT%{python_sitearch}
%endif
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc wxPython/docs wxPython/demo wxPython/licence/ wxPython/samples
%{_bindir}/*
%{python_sitearch}/*
%{python_sitelib}/*egg-info

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/wx-*/wx/wxPython
%{_includedir}/wx-*/wx/wxPython/*.h
%dir %{_includedir}/wx-*/wx/wxPython/i_files
%{_includedir}/wx-*/wx/wxPython/i_files/*



%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 3.0.1.1-2
- Rebuild

