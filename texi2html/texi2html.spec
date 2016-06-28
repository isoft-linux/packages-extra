Name: texi2html
Version: 5.0
Release: 4
# GPLv2+ is for the code
# OFSFDL (Old FSF Documentation License) for the documentation
# CC-BY-SA or GPLv2 for the images
License: GPLv2+ and OFSFDL and (CC-BY-SA or GPLv2)
Group: Applications/Text
Summary: A highly customizable texinfo to HTML and other formats translator
Source0: http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.bz2
# Do not install bundled Unicode-EastAsianWidth, bug #1154436,
# <https://savannah.nongnu.org/bugs/?43456>
Patch0: texi2html-5.0-Do-not-install-Unicode-EastAsianWidth-if-external-is.patch
# Do not install bundled libintl-perl, <https://savannah.nongnu.org/bugs/?43457>
Patch1: texi2html-5.0-Do-not-install-libintl-perl-if-external-is-used.patch
URL: http://www.nongnu.org/texi2html/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: perl >= 5.004
Requires: latex2html
# autotools for the unbundling patches
BuildRequires: autoconf automake
BuildRequires: latex2html  gettext
#BuildRequires: latex2html tetex-tex4ht gettext
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Locale::Messages)
BuildRequires: perl(Text::Unidecode)
BuildRequires: perl(Unicode::EastAsianWidth)
# not detected automatically because it is required at runtime based on
# user configuration
Requires: perl(Locale::Messages)
Requires: perl(Text::Unidecode)
Requires: perl(Unicode::EastAsianWidth)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
The basic purpose of texi2html is to convert Texinfo documents into HTML, 
and other formats.  Configuration files written in perl provide fine degree 
of control over the final output, allowing most every aspect of the final 
output not specified in the Texinfo input file to be specified.  

%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Remove bundled modules
rm -r lib
# Regenerate build script because of the patch
aclocal -I m4
automake --add-missing
autoconf

%build
%configure --with-external-libintl-perl=yes \
    --with-external-Unicode-EastAsianWidth=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# directories shared by all the texinfo implementations for common
# config files, like htmlxref.cnf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texinfo $RPM_BUILD_ROOT%{_sysconfdir}/texinfo

%find_lang %{name}
%find_lang %{name}_document

%check
#make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir > /dev/null 2>&1 || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir > /dev/null 2>&1 || :
fi

%files -f %{name}.lang -f %{name}_document.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO %{name}.init
%{_bindir}/%{name}
%{_datadir}/texinfo/html/%{name}.html
%{_mandir}/man*/%{name}*
%{_infodir}/%{name}.info*
%{_datadir}/texinfo/init/*.init
%dir %{_datadir}/%{name}/i18n/
%{_datadir}/%{name}/i18n/*
%dir %{_datadir}/%{name}/images/
%{_datadir}/%{name}/images/*
%dir %{_datadir}/texinfo
%dir %{_sysconfdir}/texinfo

%changelog
* Fri May 06 2016 fj <fujiang.zhu@i-soft.com.cn> - 5.0-4
- rebuilt for xen

