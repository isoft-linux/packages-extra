Name:           fsharp
Version:        3.1.1.32
Release:        4.1
Summary:        F# compiler, core library and core tools
License:        Apache-2.0
Group:          Development/Languages/Other
Url:            http://fsharp.github.io
Source:         https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
Source1:        fsharp.rpmlintrc

BuildRequires:  automake
BuildRequires:  mono
BuildRequires:  fdupes
BuildArch:      noarch

%description
F# is a mature, open source, functional-first programming language
which empowers users and organizations to tackle complex computing
problems with simple, maintainable and robust code. It is used in
a wide range of application areas and is available across multiple
platforms.

%prep
%setup -q
%build
autoreconf

%configure
make

%install
make install DESTDIR=%{buildroot}

rm -rf ${RPM_BUILD_ROOT}%{_prefix}/lib/mono/monodroid
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/lib/mono/monotouch
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/lib/mono/xbuild

%files
%defattr(-,root,root)
%{_bindir}/fsharpc
%{_bindir}/fsharpi
%{_bindir}/fsharpiAnyCpu
%{_prefix}/lib/mono/2.0/policy.2.0.FSharp.Core.dll
%{_prefix}/lib/mono/2.0/policy.2.3.FSharp.Core.dll
%{_prefix}/lib/mono/4.0/FSharp.Core.dll
%{_prefix}/lib/mono/4.0/FSharp.Core.xml
%{_prefix}/lib/mono/4.0/FSharp.Core.optdata
%{_prefix}/lib/mono/4.0/FSharp.Core.sigdata
%{_prefix}/lib/mono/4.5/FSharp.Build.dll
%{_prefix}/lib/mono/4.5/FSharp.Build.xml
%{_prefix}/lib/mono/4.5/FSharp.Compiler.Interactive.Settings.dll
%{_prefix}/lib/mono/4.5/FSharp.Compiler.Interactive.Settings.xml
%{_prefix}/lib/mono/4.5/FSharp.Compiler.Server.Shared.dll
%{_prefix}/lib/mono/4.5/FSharp.Compiler.Server.Shared.xml
%{_prefix}/lib/mono/4.5/FSharp.Compiler.dll
%{_prefix}/lib/mono/4.5/FSharp.Compiler.xml
%{_prefix}/lib/mono/4.5/FSharp.Core.dll
%{_prefix}/lib/mono/4.5/FSharp.Core.xml
%{_prefix}/lib/mono/4.5/FSharp.Core.optdata
%{_prefix}/lib/mono/4.5/FSharp.Core.sigdata
%{_prefix}/lib/mono/4.5/FSharp.Data.TypeProviders.dll
%{_prefix}/lib/mono/4.5/FSharp.Data.TypeProviders.xml
%{_prefix}/lib/mono/4.5/Microsoft.FSharp.Targets
%{_prefix}/lib/mono/4.5/Microsoft.Portable.FSharp.Targets
%{_prefix}/lib/mono/4.5/fsc.exe
%{_prefix}/lib/mono/4.5/fsi.exe
%{_prefix}/lib/mono/4.5/fsiAnyCpu.exe
%{_prefix}/lib/mono/4.5/policy.2.0.FSharp.Core.dll
%{_prefix}/lib/mono/4.5/policy.2.3.FSharp.Core.dll
%{_prefix}/lib/mono/4.5/policy.3.3.FSharp.Core.dll
%{_prefix}/lib/mono/4.5/policy.4.0.FSharp.Core.dll
%{_prefix}/lib/mono/4.5/policy.4.3.FSharp.Core.dll
%{_prefix}/lib/mono/Microsoft*
%{_prefix}/lib/mono/gac/FSharp.Compiler.Interactive.Settings/
%{_prefix}/lib/mono/gac/FSharp.Compiler.Server.Shared/
%{_prefix}/lib/mono/gac/FSharp.Compiler/
%{_prefix}/lib/mono/gac/FSharp.Core/
%{_prefix}/lib/mono/gac/FSharp.Data.TypeProviders/
%{_prefix}/lib/mono/gac/policy.2.0.FSharp.Core/
%{_prefix}/lib/mono/gac/policy.2.3.FSharp.Core/
%{_prefix}/lib/mono/gac/policy.3.3.FSharp.Core/
%{_prefix}/lib/mono/gac/policy.4.0.FSharp.Core/
%{_prefix}/lib/mono/gac/policy.4.3.FSharp.Core/

%changelog
