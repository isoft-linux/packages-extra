Name: coffeescript 
Version: 1.10.0
Release: 2
Summary: A little language that compiles into JavaScript.

License: refer to LICENSE
URL: http://coffeescript.org
#https://github.com/jashkenas/coffeescript/archive/1.10.0.tar.gz
Source0: %{name}-%{version}.tar.gz

#underscore required by coffeescript Cakefile
#http://underscorejs.org/underscore.js
Source1: underscore-1.8.3.tar.gz

#vim files
Source2: vim-coffee-script-003.tar.gz

Requires: nodejs 

BuildArch: noarch

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
#setup internal underscore
mkdir lib/underscore
tar zxf %{SOURCE1} -C lib/underscore --strip-components=1 

#use internal underscore and not link to $HOME
sed -i "s|require 'underscore'|require './lib/underscore'|g" Cakefile
sed -i 's|"mkdir -p ~/.node_libraries"||g' Cakefile
sed -i 's|"ln -sfn #{lib}/lib/coffee-script #{node}"||g' Cakefile

%build

%install
./bin/cake --prefix %{buildroot}/usr install

#fix symlink
pushd %{buildroot}%{_bindir}
rm -rf cake
ln -sf %{_libdir}/coffee-script/bin/cake .
rm -rf coffee
ln -sf %{_libdir}/coffee-script/bin/coffee .
popd


mkdir -p %{buildroot}%{_datadir}/vim/vimfiles/
tar zxf %{SOURCE2} -C %{buildroot}%{_datadir}/vim/vimfiles/ --strip-components=1

rm -rf %{buildroot}%{_datadir}/vim/vimfiles/*.md
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/doc
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/test
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/Makefile
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/.git*


#remove internal underscore, it's only used in coffeescript 'Cakefile'
rm -rf %{buildroot}%{_libdir}/coffee-script/lib/underscore 

%files
%{_bindir}/*
%{_libdir}/coffee-script
%{_datadir}/vim/vimfiles/after/indent/html.vim
%{_datadir}/vim/vimfiles/after/syntax/haml.vim
%{_datadir}/vim/vimfiles/after/syntax/html.vim
%{_datadir}/vim/vimfiles/autoload/coffee.vim
%{_datadir}/vim/vimfiles/compiler/cake.vim
%{_datadir}/vim/vimfiles/compiler/coffee.vim
%{_datadir}/vim/vimfiles/ftdetect/coffee.vim
%{_datadir}/vim/vimfiles/ftplugin/coffee.vim
%{_datadir}/vim/vimfiles/indent/coffee.vim
%{_datadir}/vim/vimfiles/syntax/coffee.vim

%changelog
* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 1.10.0-2
- Initial build


