Name:		fox
# http://www.fox-toolkit.org/faq.html#VERSION
# For now, use stable one
Version:	1.6.50
Release:	5%{?dist}
Summary:	C++ based Toolkit for developing Graphical User Interfaces

License:	LGPLv2+ with exceptions
URL:		http://www.fox-toolkit.org/   
Source0:	http://ftp.fox-toolkit.org/pub/%{name}-%{version}.tar.gz
# Change Adie.stx path
Patch0:	fox-1.6.49-adie-syspath.patch
# Fix libCHART.so linkage (already fixed in 1.7.x branch)
Patch1:	fox-1.6.49-libCHART-linkage.patch

#fox is not a multilingual friendly toolkit.
#acctually, the font processing is very simple in fox toolkit.
#it's load a font "Sans" globally, and not match font via "text".
#that's to say, it can not display multilinggual at same time very well.
#A better way to fix it is "according to text to display, detect FcCharset",
#but the API of fox will not support it since as I said, it load a font once and globally.
#!!!!!!And, we force font match of Sans/Serif to "English font" in fontconfig.
#here will have a problem that Fox will get an English font even when under none en locale.
#But remember, the root cause is not our fault(althouth we force font matching to English font)
#Here is a dirty fix, at least for CJK.
#By Cjacker.
Patch2: fox-atleast-cjk-respect-locale-for-fclang.patch

BuildRequires:	bzip2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libGL-devel
BuildRequires:	libGLU-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libXft-devel
BuildRequires:	libXi-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXrender-devel
# 1.7.x can use libwebp
#BuildRequires:	libwebp-devel
BuildRequires:	zlib-devel
# Due to Patch1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

%description
FOX is a C++ based Toolkit for developing Graphical User Interfaces 
easily and effectively. It offers a wide, and growing, collection of 
Controls, and provides state of the art facilities such as drag and drop,
selection, as well as OpenGL widgets for 3D graphical manipulation.
FOX also implements icons, images, and user-convenience features such as 
status line help, and tooltips.  Tooltips may even be used for 3D
objects.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Utility applications based on %{name}
Requires:	%{name}%{?isa} = %{version}-%{release}
# Note that 1.7.x has switched to GPLv3+
License:	GPLv2+

%description	utils
This package contains some utility applications based on
%{name}.

%package	doc
Summary:	Documentation files for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains some documentation files for
%{name}.

%prep
%setup -q
%patch0 -p1 -b .syspath
%patch1 -p1 -b .linkage
%patch2 -p1

# Patch1
autoreconf -fi

# Honor Fedora compilar flags
touch -r configure.ac{,.timestamp}
sed -i.flags \
	-e '\@^CXXFLAGS=""@d' \
	configure.ac configure
touch -r configure.ac{.timestamp,}

for f in \
	AUTHORS \
	doc/{styles,menu}.css
do
	mv $f{,.iso}
	iconv -f ISO-8859-1 -t UTF-8 -o $f{,.iso}
	touch -r $f{.iso,}
	rm -f $f.iso
done

%build
%configure \
	--disable-static \
	--with-xim \
%if 0
	--enable-webp \
%endif
	%{nil}
make %{?_smp_mflags}

%install
%make_install \
	INSTALL="install -p"

rm -f %{buildroot}%{_libdir}/lib*.la

# Change Adie.stx path
mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_bindir}/Adie.stx %{buildroot}%{_datadir}/%{name}/
chmod 0644 %{buildroot}%{_datadir}/%{name}/Adie.stx

# Rename too generic names
# Create desktop file for GUI
mkdir -p %{buildroot}%{_libexecdir}/fox
mkdir -p %{buildroot}%{_datadir}/applications
for bin in %{buildroot}%{_bindir}/*
do
	name=$(basename $bin)
	[ "${name%.stx}" = "${name}" ] || continue
	[ "${name#fox-config}" = "${name}" ] || continue
	mv %{buildroot}%{_bindir}/${name} %{buildroot}%{_libexecdir}/fox/
	cat > %{buildroot}%{_bindir}/fox-${name} <<EOF
#!/bin/sh
export PATH=%{_libexecdir}/%{name}:\$PATH
exec ${name} \$@
EOF
	chmod 0755 %{buildroot}%{_bindir}/fox-${name}
	mv %{buildroot}/%{_mandir}/man1/{,fox-}$name.1

	[ "$name" = reswrap ] && continue
	[ "$name" = adie ] && EXTRA_CATEGORY="TextEditor;"
	cat > %{buildroot}%{_datadir}/applications/fox-${name}.desktop <<EOF
[Desktop Entry]
Name=fox-${name}
Comment=${name}
TryExec=fox-${name}
Exec=fox-${name}
Terminal=false
Type=Application
Categories=Utility;$EXTRA_CATEGORY
EOF
	desktop-file-validate %{buildroot}%{_datadir}/applications/fox-${name}.desktop
done

# Move html files to -doc
rm -rf doc-files
mkdir doc-files
mv %{buildroot}%{_docdir}/%{name}-*/html doc-files
rm -f doc-files/html/filter.pl

%check
# Binary files created under tests/ directory are actually GUI test
# program, so nothing can do here.
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
	
%files
%doc	AUTHORS
%doc	LICENSE*
%doc	README
%dir	%{_datadir}/%{name}
%{_libdir}/libFOX-1.6.so.*
%{_libdir}/libCHART-1.6.so.*

%files	devel
%doc	ADDITIONS
%doc	TRACING

%{_bindir}/fox-config*
%{_libdir}/pkgconfig/fox.pc
%{_libdir}/libFOX-1.6.so
%{_libdir}/libCHART-1.6.so
%{_includedir}/fox-1.6/

%files	utils
%{_bindir}/fox-*
%exclude	%{_bindir}/fox-config*
%dir	%{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_datadir}/%{name}/*.stx
%{_datadir}/applications/*desktop
%{_mandir}/man1/fox-*

%files	doc
%doc	doc-files/html

%changelog
