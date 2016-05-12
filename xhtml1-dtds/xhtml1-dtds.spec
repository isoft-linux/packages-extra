%global date    20020801

Name:           xhtml1-dtds
Version:        1.0
Release:        %{date}.13%{?dist}.1
Summary:        XHTML 1.0 document type definitions

Group:          Applications/Text
# W3C Software License for DTDs etc:
# http://www.w3.org/Consortium/Legal/IPR-FAQ-20000620#DTD
License:        W3C
URL:            http://www.w3.org/TR/2002/REC-xhtml1-%{date}/
# Source0 generated with Source99, see comments in the script
Source0:        %{name}-%{date}.tar.xz
Source1:        %{name}.catalog.xml
Source99:       %{name}-prepare-tarball.sh
Patch0:         %{name}-sgml-catalog.patch
Patch1:         %{name}-sgml-dcl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  libxml2 >= 2.4.8
Requires:       libxml2 >= 2.4.8
Requires:       xml-common
Requires:       sgml-common
Requires(post): /usr/bin/xmlcatalog
Requires(preun): /usr/bin/xmlcatalog

%description
This provides the DTDs of the Second Edition of XHTML 1.0, a reformulation
of HTML 4 as an XML 1.0 application, and three DTDs corresponding to the
ones defined by HTML 4. The semantics of the elements and their attributes
are defined in the W3C Recommendation for HTML 4. These semantics provide
the foundation for future extensibility of XHTML.


%prep
%setup -q -n xhtml1-20020801
%patch0 -p0
%patch1 -p1
cp -p %{SOURCE1} DTD/catalog.xml


%build


%install
rm -rf $RPM_BUILD_ROOT

# Note: documentation is not shipped; the W3C Documentation License is not an
# acceptable one per Fedora licensing guidelines.

mkdir -p $RPM_BUILD_ROOT%{_datadir}/xml/xhtml/1.0
cp -p DTD/* $RPM_BUILD_ROOT%{_datadir}/xml/xhtml/1.0

# XML catalog:

xpkg() {
  xmlcatalog --noout --add "$1" "$2" \
    file://%{_datadir}/xml/xhtml/1.0/catalog.xml \
    $RPM_BUILD_ROOT%{_sysconfdir}/xml/%{name}-%{version}-%{release}.xml
}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xml
xmlcatalog --noout --create \
  $RPM_BUILD_ROOT%{_sysconfdir}/xml/%{name}-%{version}-%{release}.xml
xpkg delegatePublic "-//W3C//DTD XHTML 1.0 "
xpkg delegatePublic "-//W3C//ENTITIES Latin 1 for XHTML"
xpkg delegatePublic "-//W3C//ENTITIES Special for XHTML"
xpkg delegatePublic "-//W3C//ENTITIES Symbols for XHTML"
for i in xhtml1 2002/REC-xhtml1-%{date} ; do
  xpkg delegateSystem http://www.w3.org/TR/$i/DTD/
  xpkg delegateURI http://www.w3.org/TR/$i/DTD/
done
ln -s %{name}-%{version}-%{release}.xml \
  $RPM_BUILD_ROOT%{_sysconfdir}/xml/%{name}.xml

# SGML catalog:

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
cd $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch %{name}-%{version}-%{release}.soc
ln -s %{name}-%{version}-%{release}.soc %{name}.soc
cd -


%clean
rm -rf $RPM_BUILD_ROOT


%post
cd %{_sysconfdir}/xml
[ -e catalog ] || /usr/bin/xmlcatalog --noout --create catalog
/usr/bin/xmlcatalog --noout --add \
    nextCatalog %{name}-%{version}-%{release}.xml "" catalog >/dev/null
cd - >/dev/null
/usr/bin/xmlcatalog --sgml --noout --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/xml/xhtml/1.0/xhtml.soc >/dev/null
:

%preun
/usr/bin/xmlcatalog --noout --del \
    %{name}-%{version}-%{release}.xml \
    %{_sysconfdir}/xml/catalog >/dev/null
/usr/bin/xmlcatalog --sgml --noout --del \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/xml/xhtml/1.0/xhtml.soc >/dev/null
:


%files
%defattr(644,root,root,755)
%ghost %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc
%{_sysconfdir}/sgml/%{name}.soc
%{_sysconfdir}/xml/%{name}*.xml
%{_datadir}/xml/xhtml/


%changelog
* Thu May 05 2016 fj <fujiang.zhu@i-soft.com.cn> - 1.0-20020801.13.1
- rebuilt for libvirt

