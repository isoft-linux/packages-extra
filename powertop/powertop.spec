Name:	    powertop	
Version:	2.7
Release:	1
Summary:	PowerTOP is a Linux tool to diagnose issues with power consumption and power management.

Group:      Development/Debuggers	
License:    GPL	
URL:		https://01.org/zh/powertop
Source0:	%{name}-%{version}.tar.gz

%description
PowerTOP is a Linux tool to diagnose issues with power consumption and power management.

In addition to being a diagnostic tool, PowerTOP also has an interactive mode where the user can experiment various power management settings for cases where the Linux distribution has not enabled these settings.

%prep
%setup -q

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%find_lang powertop

%files -f powertop.lang
%{_sbindir}/powertop
%{_mandir}/man8/powertop.8.gz



%changelog

