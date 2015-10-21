%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           translate-toolkit
Version:        1.9.0
Release:        5%{?dist}
Summary:        Tools to assist with translation and software localization

Group:          Development/Tools
License:        GPLv2+
URL:            http://translate.sourceforge.net/wiki/toolkit/index
Source0:        http://downloads.sourceforge.net/project/translate/Translate%20Toolkit/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Common patches
Patch0:         translate-toolkit-1.8.1-stoplist.patch
Patch1:         translate-toolkit-1.5.0-langmodel_dir.patch


BuildArch:      noarch
BuildRequires:  python-devel
# The following are needed for man page generation
BuildRequires:  python-lxml
BuildRequires:  python-simplejson
BuildRequires:  python-vobject
Requires:       gettext-libs
Requires:       python-enchant
Requires:       python-iniparse
Requires:       python-Levenshtein
Requires:       python-lxml
%ifarch %{ix86}
Requires:       python-psyco
%endif
Requires:       python-simplejson
Requires:       python-vobject
Requires:       aeidon


%description
A set of tools for managing translation and software localization via 
Gettext PO or XLIFF format files.

Including:
  * Convertors: convert from various formats to PO or XLIFF
  * Formats:
    * Core localization formats - XLIFF and Gettext PO
    * Other localization formats - TMX, TBX, Qt Linguist (.ts), 
           Java .properties, Wordfast TM, OmegaT glossary
    * Compiled formats: Gettext MO, Qt .qm
    * Other formats - OpenDocument Format (ODF), text, HTML, CSV, INI, 
            wiki (MediaWiki, DokuWiki), iCal
    * Specialised - OpenOffice.org GSI/SDF, PHP,
            Mozilla (.dtd, .properties, etc), Symbian,
            Innosetup, tikiwiki, subtitles
  * Tools: count, search, debug, segment and pretranslate localization 
            files. Extract terminology. Pseudo-localize
  * Checkers: validate translations with over 45 checks

%package devel
Summary:        Development API for %{name} applications
Group:          Development/Tools
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains Translate Toolkit API 
documentation for developers wishing to build new tools for the 
toolkit or to use the libraries in other localization tools.


%prep
%setup -q
%patch0 -p1 -b .stoplist
%patch1 -p1 -b .langmodel_dir


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# create manpages
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
for program in $RPM_BUILD_ROOT/%{_bindir}/*; do
    case $(basename $program) in
      pocompendium|poen|pomigrate2|popuretext|poreencode|posplit|\
      pocount|poglossary|tmserver|build_tmdb|\
      junitmsgfmt)
       ;;
      *)
        LC_ALL=C PYTHONPATH=. $program --manpage \
          >  $RPM_BUILD_ROOT/%{_mandir}/man1/$(basename $program).1 \
          || rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/$(basename $program).1
          ;;
    esac
done

# remove documentation files from site-packages
rm -r $RPM_BUILD_ROOT/%{python_sitelib}/translate/doc
rm $RPM_BUILD_ROOT/%{python_sitelib}/translate/{COPYING,ChangeLog,LICENSE,README}
rm $RPM_BUILD_ROOT/%{python_sitelib}/translate/{convert,filters,tools}/TODO
rm $RPM_BUILD_ROOT/%{python_sitelib}/translate/misc/README

# Move data files to /usr/share
mkdir  $RPM_BUILD_ROOT/%{_datadir}/translate-toolkit
mv $RPM_BUILD_ROOT/%{python_sitelib}/translate/share/stoplist* $RPM_BUILD_ROOT/%{_datadir}/translate-toolkit
mv $RPM_BUILD_ROOT/%{python_sitelib}/translate/share/langmodels $RPM_BUILD_ROOT/%{_datadir}/translate-toolkit
rmdir $RPM_BUILD_ROOT/%{python_sitelib}/translate/share


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc translate/ChangeLog translate/COPYING translate/README
%doc translate/doc/user/toolkit-[a-z]*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/translate-toolkit
%{python_sitelib}/translate*

%files devel
%defattr(-,root,root,-)
%doc translate/doc/api/*


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
