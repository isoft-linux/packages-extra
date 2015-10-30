%{!?python3_sitelib: %define python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global __python %{__python3}

Name:		gaupol
Version:	0.25
Release:	5%{?dist}
Summary:	Subtitle editor

License:	GPLv3+
URL:		http://home.gna.org/gaupol
Source0:	http://download.gna.org/gaupol/0.19/%{name}-%{version}.tar.xz
BuildArch:	noarch

BuildRequires:	python3-devel
BuildRequires:	desktop-file-utils, gettext, doxygen, intltool
BuildRequires:	python3-setuptools
Requires:	python3-enchant, python3-chardet
Requires:	aeidon

%description
Editor for text-based subtitle files. It supports multiple subtitle file
formats and provides means of correcting texts and timing subtitles to match
video. The user interface is designed with attention to batch processing of
multiple documents and convenience of translating.

%package -n aeidon
Summary: Package for reading, writing and manipulating text-based subtitle files

%description -n aeidon
This is a Python package for reading, writing and manipulating
text-based subtitle files. It is separate from the gaupol package,
which provides a subtitle editor application with a GTK+ user
interface.

%prep
%setup -q
sed -i -e "s/Encoding=UTF-8//" data/%{name}.desktop.in

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%find_lang %{name}
desktop-file-install					\
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications		\
--add-category AudioVideoEditing			\
$RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING CREDITS README NEWS TODO
%{_bindir}/gaupol
%{python3_sitelib}/gaupol*
%{_datadir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*/*/apps/%{name}.*
%{_mandir}/man1/gaupol.1*

%files -n aeidon
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING CREDITS README.aeidon NEWS TODO
%{python3_sitelib}/aeidon

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 0.25-5
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.
