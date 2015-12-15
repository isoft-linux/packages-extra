Name: vim-elixir
Version: 0.1
Release: 2.git
Summary: Vim configuration files for Elixir

License: Apache 
URL: https://github.com/elixir-lang/vim-elixir
Source0: %{name}.tar.gz 

Requires: vim elixir 
Requires: ruby

BuildArch: noarch

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}/vim/vimfiles
tar zxf %{SOURCE0} -C %{buildroot}%{_datadir}/vim/vimfiles --strip-components=1

rm -rf %{buildroot}%{_datadir}/vim/vimfiles/LICE*
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/.[a-z]*
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/*.md
rm -rf %{buildroot}%{_datadir}/vim/vimfiles/Gem*

%files
%{_datadir}/vim/vimfiles/compiler/exunit.vim
%{_datadir}/vim/vimfiles/ftdetect/eelixir.vim
%{_datadir}/vim/vimfiles/ftdetect/elixir.vim
%{_datadir}/vim/vimfiles/ftplugin/eelixir.vim
%{_datadir}/vim/vimfiles/ftplugin/elixir.vim
%{_datadir}/vim/vimfiles/indent/eelixir.vim
%{_datadir}/vim/vimfiles/indent/elixir.vim
%{_datadir}/vim/vimfiles/spec/indent/anonymous_functions_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/blocks_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/case_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/cond_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/documentation_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/embedded_elixir_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/if_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/lists_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/pipeline_spec.rb
%{_datadir}/vim/vimfiles/spec/indent/tuples_spec.rb
%{_datadir}/vim/vimfiles/spec/spec_helper.rb
%{_datadir}/vim/vimfiles/spec/syntax/default_argument_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/embedded_elixir_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/guard_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/heredoc_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/list_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/records_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/sigil_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/struct_spec.rb
%{_datadir}/vim/vimfiles/spec/syntax/variable_spec.rb
%{_datadir}/vim/vimfiles/syntax/eelixir.vim
%{_datadir}/vim/vimfiles/syntax/elixir.vim

%changelog
* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 0.1-2.git
- Initial build




