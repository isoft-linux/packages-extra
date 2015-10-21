Name:		fop
Version:    	2.0 
Release:	1
Summary:	A print formatter driven by XSL formatting objects (XSL-FO)

Group:		Extra/Runtime/Utility/Java
License:	Apache License, version 2.0
URL:	    	http://xmlgraphics.apache.org/fop/	
Source0:	http://apache.01link.hk/xmlgraphics/fop/binaries/fop-%{version}-bin.tar.gz
#wrapper script
Source1:    fop

#it's platform independent.
BuildArch:  noarch

#Not enable requires here, Either openjdk or jamvm can run fop properly.
#Will detect in fop wrapper script.
#Requires: 
%description
Apache FOP (Formatting Objects Processor) is a print formatter driven by XSL formatting objects (XSL-FO)
and an output independent formatter. 

It is a Java application that reads a formatting object (FO) tree 
and renders the resulting pages to a specified output. 
Output formats currently supported include PDF, PS, PCL, AFP, XML (area tree representation), 
Print, AWT and PNG, and to a lesser extent, RTF and TXT. 

The primary output target is PDF.

%prep

%build
%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fop
tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{_datadir}/fop --strip-components=1
install -Dm0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop

%files
%dir %{_datadir}/fop
%{_datadir}/fop/*
%{_bindir}/fop

%changelog
* Sun Oct 2 2014 Cjacker <cjacker@gmail.com>
- create package
- add a wrapper script to detect JAVA_HOME or jamvm
