Name:           rlwrap
Version:        0.42
Release:        3%{?dist}
Summary:        Wrapper for GNU readline

License:        GPLv2+
URL:            http://utopia.knoware.nl/~hlub/rlwrap/
Source0:        http://utopia.knoware.nl/~hlub/rlwrap/rlwrap-%{version}.tar.gz

BuildRequires:  readline-devel
#Requires:       

%description
rlwrap is a 'readline wrapper' that uses the GNU readline library to
allow the editing of keyboard input for any other command. Input
history is remembered across invocations, separately for each command;
history completion and search work as in bash and completion word
lists can be specified on the command line.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
(cd $RPM_BUILD_ROOT%{_datadir}/rlwrap/filters
# these are not scripts
chmod -x README
chmod -x RlwrapFilter.*pm
)


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/rlwrap
%{_mandir}/*/rlwrap.*
%{_mandir}/man3/RlwrapFilter.*
%{_datadir}/rlwrap



%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 0.42-3
- Initial build

