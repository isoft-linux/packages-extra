# These are the build option passed to ./configure command
%global build_options  --enable-m17n --enable-unicode --enable-nls --with-editor=/bin/vi --with-mailer="gnome-open mailto:%s" --with-browser=gnome-open --with-charset=UTF-8 --with-gc --with-termlib=ncurses --enable-nntp --enable-gopher --enable-image=x11,fb --with-imagelib=gtk2 --enable-keymap=w3m

# This is for file encoding/conversions
%global   with_utf8 1
%{?perl_default_filter}
%global __requires_exclude perl\\(w3mhelp-

Name:     w3m
Version:  0.5.3
Release:  22%{?dist}
# UCD is added for EastAsianWidth.txt source
License:  MIT and UCD
URL:      http://w3m.sourceforge.net/
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  gettext-devel
BuildRequires:  automake
BuildRequires:  gtk2-devel
BuildRequires:  gdk-pixbuf2-devel
%ifnarch s390 s390x
BuildRequires:  gpm-devel
%endif
BuildRequires:  gc-devel
BuildRequires:  nkf
BuildRequires:  lynx

# This is needed for perl files
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: perl(NKF)

## re-compressed bzip2 instead of gzip
Source0: http://downloads.sourceforge.net/w3m/%{name}-%{version}.tar.gz

Source1:  w3mconfig

# Change for function call GC_get_warn_proc()
# https://sourceforge.net/tracker/?func=detail&aid=3595876&group_id=39518&atid=425441
Patch0:  %{name}-rh555467_FTBFS.patch

# w3mimgdisplay need to be linked with -lX11 to build against gcc 4.5
# https://sourceforge.net/tracker/?func=detail&aid=3126430&group_id=39518&atid=425441
Patch1:  %{name}-rh566101_Fix-DSO-X11.patch

# verify SSL certificates by default. SSL support really is pointless
# without doing that. Also disable use of SSLv2 by default as it's 
# insecure, deprecated, dead since last century.
# https://sourceforge.net/tracker/?func=detail&aid=3595801&group_id=39518&atid=425441
Patch2:  %{name}-0.5.2-ssl_verify_server_on.patch

# Now glib-2.14 owns structure name file_handle
# https://sourceforge.net/tracker/?func=detail&aid=3595814&group_id=39518&atid=425441
Patch3:  %{name}-0.5.2-glibc2.14-fix_file_handle_error.patch

# Resolves a bug of when given following command w3m crashes
# w3m https://www.example.coma
# but following command works fine by giving can't load error
# w3m http://www.example.coma
# https://sourceforge.net/tracker/?func=detail&aid=3595167&group_id=39518&atid=425441
Patch4:  %{name}-rh707994-fix-https-segfault.patch

#https://sourceforge.net/tracker/?group_id=39518&atid=425441
Patch5:  %{name}-0.5.3-parallel-make.patch

Patch6:  %{name}-0.5.3-format-security.patch

Patch7:  %{name}-0.5.3-FTBFS-sys-errlist.patch

Summary:  A pager with Web browsing abilities
Provides:  webclient
Provides: text-www-browser

%description
The w3m program is a pager (or text file viewer) that can also be used
as a text-mode Web browser. W3m features include the following: when
reading an HTML document, you can follow links and view images using
an external image viewer; its internet message mode determines the
type of document from the header; if the Content-Type field of the
document is text/html, the document is displayed as an HTML document;
you can change a URL description like 'http://hogege.net' in plain
text into a link to that URL.
If you want to display the inline images on w3m, you need to install
w3m-img package as well.

%package img
Summary: A helper program to display the inline images for w3m
Requires: ImageMagick
Requires: %{name} = %{version}-%{release}

%description img
w3m-img package provides a helper program for w3m to display the inline
images on the terminal emulator in X Window System environments and the
linux framebuffer.

%prep
%setup -q
chmod 755 doc
chmod 755 doc-jp

%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1

%if %{with_utf8}
pushd doc-jp
for f in * ; do
   case $f in
      README.pre_form | README.tab )
         CHARSET=ISO-2022-JP
         ;;
      keymap.* )
         CHARSET=UTF-8
         ;;
      * )
         CHARSET=EUC-JP
         ;;
    esac
    iconv -f $CHARSET -t UTF-8 $f > $f.tmp && \
      ( touch -r $f $f.tmp ; mv $f.tmp $f ) || rm -f $f.tmp
done
popd
%endif

pushd doc
# Convert to utf-8
for file in README.m17n README.cookie; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done
popd

for file in scripts/w3mhelp-funcdesc.ja.pl.in; do
    iconv -f EUC-JP -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure %{build_options}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

mkdir -p %{buildroot}%{_sysconfdir}/w3m
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/w3m/config

rm -f doc*/w3m.1
rm -rf doc/CVS doc-jp/CVS

%find_lang w3m

%files -f w3m.lang
%doc doc NEWS
%lang(ja) %doc doc-jp
%{_datadir}/w3m/
%config(noreplace) %{_sysconfdir}/w3m/
%{_bindir}/w3m*
%lang(ja) %{_mandir}/ja/man1/w3m.1*
%{_mandir}/man1/w3m.1*
%{_mandir}/man1/w3mman.1*
%{_libexecdir}/w3m/
%exclude %{_libexecdir}/w3m/w3mimgdisplay

%files img
%{_libexecdir}/w3m/w3mimgdisplay

%changelog
