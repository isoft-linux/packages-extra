Name:    qtscriptgenerator
Summary: A tool to generate Qt bindings for Qt Script
Version: 0.2.0
Release: 12%{?dist}

License: GPLv2  
URL:     http://code.google.com/p/qtscriptgenerator/	
Source0: http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-%{version}.tar.gz

Patch1: qtscriptgenerator-0.1.0-gcc44.patch
Patch2: qtscriptgenerator-src-0.1.0-no_phonon.patch

## upstreamable patches
Patch50: qtscriptgenerator-src-0.1.0-qmake_target.path.patch
# needs work
Patch51: qtscriptgenerator-kde_phonon443.patch
# fix arm ftbfs, kudos to mamba
Patch52: qtscriptgenerator-0.2.0-arm-ftbfs-float.patch
## debian patches
Patch60: memory_alignment_fix.diff

## upstream patches

# explictly BR libxslt, for xsltproc
BuildRequires: libxslt
# phonon bindings currently busted, see no_phonon patch
#BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtGui)
BuildRequires: pkgconfig(QtNetwork)
BuildRequires: pkgconfig(QtOpenGL)
BuildRequires: pkgconfig(QtSql)
BuildRequires: pkgconfig(QtSvg)
BuildRequires: pkgconfig(QtUiTools)
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: pkgconfig(QtXml)
BuildRequires: pkgconfig(QtXmlPatterns)

# not strictly required, but the expectation would be for the 
# bindings to be present
Requires: qtscriptbindings = %{version}-%{release}

%description
Qt Script Generator is a tool to generate Qt bindings for Qt Script.

%package -n qtscriptbindings 
Summary: Qt bindings for Qt Script
Provides: qtscript-qt = %{version}-%{release}
%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
%description -n qtscriptbindings
Bindings providing access to substantial portions of the Qt API
from within Qt Script.


%prep
%setup -q -n %{name}-src-%{version}

%patch1 -p0 -b .gcc44
%patch2 -p1 -b .no_phonon

%patch50 -p1 -b .qmake_target.path
%patch51 -p1 -b .kde_phonon
# I *think* we can do this unconditionally, but I'd like to
# investigate more in-depth first
%ifarch %{arm}
%patch52 -p1 -b .arm_ftbfs_float
%endif

%patch60 -p1 -b .memory_alignment


%build

# workaround buildsys bogosity, see also:
# http://code.google.com/p/qtscriptgenerator/issues/detail?id=38
export INCLUDE=%{_qt4_headerdir}

pushd generator 
%{_qt4_qmake}
make %{?_smp_mflags}
./generator
popd

pushd qtbindings
%{_qt4_qmake}
make %{?_smp_mflags}
popd

pushd tools/qsexec/src
%{_qt4_qmake}
make  %{?_smp_mflags}
popd


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}%{_qt4_plugindir}/script/
# install doesn't do symlinks
cp -a plugins/script/libqtscript* \
  %{buildroot}%{_qt4_plugindir}/script/

cp -a tools/qsexec/README.TXT README.qsexec
install -D -p -m755 tools/qsexec/qsexec %{buildroot}%{_bindir}/qsexec

install -D -p -m755 generator/generator %{buildroot}%{_qt4_bindir}/generator


%clean
rm -rf %{buildroot} 


%files
%defattr(-,root,root,-)
%{_qt4_bindir}/generator

%files -n qtscriptbindings
%defattr(-,root,root,-)
%doc README
%doc LICENSE.LGPL LGPL_EXCEPTION.txt
%doc README.qsexec 
%doc doc/
%doc examples/
%{_bindir}/qsexec
%{_qt4_plugindir}/script/libqtscript_core.so*
%{_qt4_plugindir}/script/libqtscript_gui.so*
%{_qt4_plugindir}/script/libqtscript_network.so*
%{_qt4_plugindir}/script/libqtscript_opengl.so*
#{_qt4_plugindir}/script/libqtscript_phonon.so*
%{_qt4_plugindir}/script/libqtscript_sql.so*
%{_qt4_plugindir}/script/libqtscript_svg.so*
%{_qt4_plugindir}/script/libqtscript_uitools.so*
%{_qt4_plugindir}/script/libqtscript_webkit.so*
%{_qt4_plugindir}/script/libqtscript_xml.so*
%{_qt4_plugindir}/script/libqtscript_xmlpatterns.so*


%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.2.0-12
- Rebuild

* Thu Oct 22 2015 Cjacker <cjacker@foxmail.com> - 0.2.0-11
- Initial build

