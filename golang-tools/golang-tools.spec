%define debug_package %{nil}
Name: golang-tools
 
Version: 1.7
Release: 2
Summary: Various packages and tools that support the Go programming language

License: Refer to LICENSE 
URL: https://github.com/golang/tools


#git clone https://github.com/golang/tools.git
Source0: tools.tar.gz
#git clone https://github.com/kisielk/errcheck.git
Source1: errcheck.tar.gz
#git clone https://github.com/kisielk/gotool.git
Source2: gotool.tar.gz
#git clone https://github.com/nsf/gocode.git
Source3: gocode.tar.gz
#git clone https://github.com/rogpeppe/godef.git
Source4: godef.tar.gz
#git clone https://github.com/bytbox/golint.git
Source6: golint.tar.gz
#https://github.com/9fans/go.git
Source7: go.tar.gz

BuildRequires: golang	
Requires: golang

Provides: gocode godef golint errcheck gorename oracle goimports
%description
%{summary}

%prep
%setup -q -c
rm -rf tools

#set up dir layout as golang requires.
mkdir -p src/golang.org/x
tar xf %{SOURCE0} -C src/golang.org/x

mkdir -p src/github.com/kisielk/
tar xf %{SOURCE1} -C src/github.com/kisielk/
tar xf %{SOURCE2} -C src/github.com/kisielk/
tar xf %{SOURCE3} -C .

#mkdir -p src/github.com/rogpeppe
#tar xf %{SOURCE4} -C src/github.com/rogpeppe

tar xf %{SOURCE6} -C .

mkdir -p src/9fans.net
tar xf %{SOURCE7} -C src/9fans.net

%build
export GOPATH=`pwd`

pushd gocode
go build
popd

pushd golint
go build
popd

pushd src/github.com/kisielk/errcheck
go build
popd

#pushd src/github.com/rogpeppe/godef
#go build
#popd

#pushd src/golang.org/x/tools/cmd/oracle
#go build
#popd

pushd src/golang.org/x/tools/cmd/goimports
go build
popd

pushd src/golang.org/x/tools/cmd/gorename
go build
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 gocode/gocode %{buildroot}%{_bindir}
install -m0755 golint/golint %{buildroot}%{_bindir}
install -m0755 src/github.com/kisielk/errcheck/errcheck %{buildroot}%{_bindir}
#install -m0755 src/github.com/rogpeppe/godef/godef %{buildroot}%{_bindir}
#install -m0755 src/golang.org/x/tools/cmd/oracle/oracle %{buildroot}%{_bindir}
install -m0755 src/golang.org/x/tools/cmd/goimports/goimports %{buildroot}%{_bindir}
install -m0755 src/golang.org/x/tools/cmd/gorename/gorename %{buildroot}%{_bindir}

%files
%{_bindir}/*

%changelog
* Thu Nov 24 2016 cjacker - 1.7-2
- Update and rebuild with golang 1.7

* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 1.5.2-2
- Initial build


