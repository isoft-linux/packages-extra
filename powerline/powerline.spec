Name:           powerline
Version:        2.3
Release:        1%{?dist}

Summary:        The ultimate status-line/prompt utility
License:        MIT
Url:            https://github.com/powerline/powerline

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  fdupes
BuildRequires:  fontconfig
BuildRequires:  tmux
BuildRequires:  vim

Requires:       python
Requires:       fontconfig

Source0:        https://github.com/powerline/powerline/archive/%{version}.tar.gz
Source1:        vim-powerline.metainfo.xml

%description
Powerline is a status-line plugin for vim, and provides status-lines and prompts
for several other applications, including zsh, bash, tmux, IPython, Awesome and
Qtile.

%package docs
Summary: Powerline Documentation

%description docs
This package provides the powerline documentation.

%package -n vim-powerline
Summary: Powerline VIM plugin
BuildArch: noarch
Requires: vim
Requires: %{name} = %{version}-%{release}
Obsoletes: vim-plugin-powerline
Provides: vim-plugin-powerline

%description -n vim-powerline
Powerline is a status-line plugin for vim, and provides status-lines and
prompts.

%package -n tmux-powerline
Summary: Powerline for tmux
BuildArch: noarch
Requires: tmux
Requires: %{name} = %{version}-%{release}

%description -n tmux-powerline
Powerline for tmux.

Add

    source /usr/share/tmux/powerline.conf

to your ~/.tmux.conf file.

%prep
%setup -q

%build
# nothing to build

%install
sed -i -e "/DEFAULT_SYSTEM_CONFIG_DIR/ s@None@'%{_sysconfdir}/xdg'@" powerline/config.py
sed -i -e "/TMUX_CONFIG_DIRECTORY/ s@BINDINGS_DIRECTORY@'/usr/share'@" powerline/config.py
CFLAGS="%{optflags}" \
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --optimize=1

# build docs
pushd docs
%__make html SPHINXBUILD=/usr/bin/sphinx-build
%__rm _build/html/.buildinfo
# A structure gets initialized while building the docs with os.environ.
# This works around an rpmlint error with the build dir being in a file.
sed -i -e 's/abuild/user/g' _build/html/develop/extensions.html

%__make man SPHINXBUILD=/usr/bin/sphinx-build
popd

# config
install -d -m0755 %{buildroot}%{_sysconfdir}/xdg/%{name}
cp -a powerline/config_files/* %{buildroot}%{_sysconfdir}/xdg/%{name}/

# fonts
install -d -m0755 %{buildroot}%{_sysconfdir}/fonts/conf.d
install -d -m0755 %{buildroot}%{_datadir}/fonts/truetype
install -d -m0755 %{buildroot}%{_datadir}/fontconfig/conf.avail

install -m0644 font/PowerlineSymbols.otf %{buildroot}%{_datadir}/fonts/truetype/PowerlineSymbols.otf
install -m0644 font/10-powerline-symbols.conf %{buildroot}%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf

ln -s %{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf %{buildroot}%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf

# manpages
%__install -d -m0755 %{buildroot}%{_datadir}/man/man1
for f in powerline-config.1 powerline-daemon.1 powerline-lint.1 powerline.1; do
%__install -m0644 docs/_build/man/$f %{buildroot}%{_datadir}/man/man1/$f
done

# awesome
install -d -m0755 %{buildroot}%{_datadir}/%{name}/awesome/
mv %{buildroot}%{python_sitelib}/powerline/bindings/awesome/powerline.lua %{buildroot}%{_datadir}/%{name}/awesome/
mv %{buildroot}%{python_sitelib}/powerline/bindings/awesome/powerline-awesome.py %{buildroot}%{_datadir}/%{name}/awesome/

# bash bindings
install -d -m0755 %{buildroot}%{_datadir}/%{name}/bash
mv %{buildroot}%{python_sitelib}/powerline/bindings/bash/powerline.sh %{buildroot}%{_datadir}/%{name}/bash/

# fish
install -d -m0755 %{buildroot}%{_datadir}/%{name}/fish
mv %{buildroot}%{python_sitelib}/powerline/bindings/fish/powerline-setup.fish %{buildroot}%{_datadir}/%{name}/fish

# i3
install -d -m0755 %{buildroot}%{_datadir}/%{name}/i3
mv %{buildroot}%{python_sitelib}/powerline/bindings/i3/powerline-i3.py %{buildroot}%{_datadir}/%{name}/i3

# ipython
install -d -m0755 %{buildroot}%{_datadir}/%{name}/ipython
mv %{buildroot}%{python_sitelib}/powerline/bindings/ipython/post_0_11.py %{buildroot}%{_datadir}/%{name}/ipython
mv %{buildroot}%{python_sitelib}/powerline/bindings/ipython/pre_0_11.py %{buildroot}%{_datadir}/%{name}/ipython

# qtile
install -d -m0755 %{buildroot}%{_datadir}/%{name}/qtile
mv %{buildroot}%{python_sitelib}/powerline/bindings/qtile/widget.py %{buildroot}%{_datadir}/%{name}/qtile

# shell bindings
install -d -m0755 %{buildroot}%{_datadir}/%{name}/shell
mv %{buildroot}%{python_sitelib}/powerline/bindings/shell/powerline.sh %{buildroot}%{_datadir}/%{name}/shell/

# tcsh
install -d -m0755 %{buildroot}%{_datadir}/%{name}/tcsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/tcsh/powerline.tcsh %{buildroot}%{_datadir}/%{name}/tcsh

# tmux plugin
install -d -m0755 %{buildroot}%{_datadir}/tmux
mv %{buildroot}%{python_sitelib}/powerline/bindings/tmux/powerline*.conf %{buildroot}%{_datadir}/tmux/

# vim plugin
install -d -m0755 %{buildroot}%{_datadir}/vim/vimfiles/plugin/
mv %{buildroot}%{python_sitelib}/powerline/bindings/vim/plugin/powerline.vim %{buildroot}%{_datadir}/vim/vimfiles/plugin/powerline.vim
rm -rf %{buildroot}%{python_sitelib}/powerline/bindings/vim/plugin
install -d -m0755 %{buildroot}%{_datadir}/vim/vimfiles/autoload/powerline
mv %{buildroot}%{python_sitelib}/powerline/bindings/vim/autoload/powerline/debug.vim %{buildroot}%{_datadir}/vim/vimfiles/autoload/powerline/debug.vim
rm -rf %{buildroot}%{python_sitelib}/powerline/bindings/vim/autoload

install -d -m0755 %{buildroot}%{_datadir}/%{name}/vim
mv %{buildroot}%{python_sitelib}/powerline/bindings/vim/__init__.py %{buildroot}%{_datadir}/%{name}/vim

# zsh
install -d -m0755 %{buildroot}%{_datadir}/%{name}/zsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/zsh/__init__.py %{buildroot}%{_datadir}/%{name}/zsh
mv %{buildroot}%{python_sitelib}/powerline/bindings/zsh/powerline.zsh %{buildroot}%{_datadir}/%{name}/zsh

# vim-powerline appdata
mkdir -p %{buildroot}%{_datadir}/appdata
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/appdata

# cleanup
%__rm -rf %{buildroot}%{python_sitelib}/%{name}/config_files

%if 0%{?fedora}
%fdupes %{buildroot}%{python_sitelib}
%endif

%files
%doc LICENSE README.rst
%{_sysconfdir}/fonts/conf.d/10-powerline-symbols.conf
%config(noreplace) %{_sysconfdir}/xdg/%{name}
%{_bindir}/powerline
%{_bindir}/powerline-config
%{_bindir}/powerline-daemon
%{_bindir}/powerline-render
%{_bindir}/powerline-lint
%{_datadir}/fontconfig/conf.avail/10-powerline-symbols.conf
%dir %{_datadir}/fonts/truetype
%{_datadir}/fonts/truetype/PowerlineSymbols.otf
%{_mandir}/man1/powerline.1*
%{_mandir}/man1/powerline-config.1*
%{_mandir}/man1/powerline-daemon.1*
%{_mandir}/man1/powerline-lint.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/awesome
%{_datadir}/%{name}/awesome/powerline.lua
%{_datadir}/%{name}/awesome/powerline-awesome.py*
%dir %{_datadir}/%{name}/bash
%{_datadir}/%{name}/bash/powerline.sh
%dir %{_datadir}/%{name}/fish
%{_datadir}/%{name}/fish/powerline-setup.fish
%dir %{_datadir}/%{name}/i3
%{_datadir}/%{name}/i3/powerline-i3.py*
%dir %{_datadir}/%{name}/ipython
%{_datadir}/%{name}/ipython/post_0_11.py*
%{_datadir}/%{name}/ipython/pre_0_11.py*
%dir %{_datadir}/%{name}/qtile
%{_datadir}/%{name}/qtile/widget.py*
%dir %{_datadir}/%{name}/shell
%{_datadir}/%{name}/shell/powerline.sh
%dir %{_datadir}/%{name}/tcsh
%{_datadir}/%{name}/tcsh/powerline.tcsh
%dir %{_datadir}/%{name}/vim
%{_datadir}/%{name}/vim/__init__.py*
%dir %{_datadir}/%{name}/zsh
%{_datadir}/%{name}/zsh/__init__.py*
%{_datadir}/%{name}/zsh/powerline.zsh
%{python_sitelib}/*

%files docs
%doc docs/_build/html

%files -n vim-powerline
%doc LICENSE README.rst
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/autoload
%dir %{_datadir}/vim/vimfiles/autoload/powerline
%{_datadir}/vim/vimfiles/autoload/powerline/debug.vim
%dir %{_datadir}/vim/vimfiles/plugin
%{_datadir}/vim/vimfiles/plugin/powerline.vim
%dir %{_datadir}/appdata
%{_datadir}/appdata/vim-powerline.metainfo.xml

%files -n tmux-powerline
%doc LICENSE README.rst
%dir %{_datadir}/tmux
%{_datadir}/tmux/powerline*.conf

%changelog
