Name: vim-go
Version: 1.3
Release: 2.git
Summary: Go (golang) support for Vim 

License: BSD
URL: https://github.com/fatih/vim-go
#git clone https://github.com/fatih/vim-go.git
Source0: vim-go.tar.gz

Requires: golang golang-tools
Requires: vim 

BuildArch: noarch

%description
Go (golang) support for Vim, which comes with pre-defined sensible settings (like auto gofmt on save), with autocomplete, snippet support, improved syntax highlighting, go toolchain commands, and more. If needed vim-go installs all necessary binaries for providing seamless Vim integration with current commands. It's highly customizable and each individual feature can be disabled/enabled easily.

%prep
%setup -q -n %{name}

%build
%install
mkdir -p %{buildroot}%{_datadir}/vim/vimfiles
tar xf %{SOURCE0} -C %{buildroot}%{_datadir}/vim/vimfiles --strip-components=1

rm -rf %{buildroot}%{_datadir}/vim/vimfiles/.git*
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/LICENSE
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/README.md
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/scripts
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/addon-info.json

%files
%{_datadir}/vim/vimfiles/*/*.vim
%{_datadir}/vim/vimfiles/*/go
%{_datadir}/vim/vimfiles/gosnippets
%{_datadir}/vim/vimfiles/*/vim-go.txt

%changelog
* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 1.3-2.git
- Initial build


