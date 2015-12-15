Name: vim-rust 
Version: 0.1 
Release: 2
Summary: vim plugin that provides Rust file detection, syntax highlighting and Code Completion via racer etc.

License: MIT and Apache
URL: https://github.com/rust-lang/rust.vim 
Source0: rust.vim.tar.gz

# https://github.com/racer-rust/vim-racer
Source1: vim-racer.tar.gz
Source2: racer.vimrc

Requires: rust racer
Requires: vim

BuildArch: noarch

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}/vim/vimfiles
tar zxf %{SOURCE0} -C %{buildroot}%{_datadir}/vim/vimfiles --strip-components=1
tar zxf %{SOURCE1} -C %{buildroot}%{_datadir}/vim/vimfiles vim-racer/plugin/racer.vim --strip-components=1

mkdir -p %{buildroot}%{_sysconfdir}/vimrc.d
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/vimrc.d/racer.vimrc

rm -rf %{buildroot}%{_datadir}/vim/vimfiles/LICE*
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/.git*
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/*.md

%files
#rust.vim
%{_datadir}/vim/vimfiles/after/syntax/rust.vim
%{_datadir}/vim/vimfiles/autoload/rust.vim
%{_datadir}/vim/vimfiles/autoload/rustfmt.vim
%{_datadir}/vim/vimfiles/compiler/cargo.vim
%{_datadir}/vim/vimfiles/compiler/rustc.vim
%{_datadir}/vim/vimfiles/doc/rust.txt
%{_datadir}/vim/vimfiles/ftdetect/rust.vim
%{_datadir}/vim/vimfiles/ftplugin/rust.vim
%{_datadir}/vim/vimfiles/indent/rust.vim
%{_datadir}/vim/vimfiles/plugin/rust.vim
%{_datadir}/vim/vimfiles/plugin/rustfmt.vim
%{_datadir}/vim/vimfiles/syntax/rust.vim
%{_datadir}/vim/vimfiles/syntax_checkers/rust/rustc.vim
#vim-racer 
%{_sysconfdir}/vimrc.d/racer.vimrc
%{_datadir}/vim/vimfiles/plugin/racer.vim

%changelog
* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 0.1-2
- Initial build


