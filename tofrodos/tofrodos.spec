Name:           tofrodos
Version:        1.7.13
Release:        6%{?dist}
Summary:        Converts text files between MSDOS and Unix file formats
License:        GPLv2
URL:            http://www.thefreecountry.com/tofrodos/
Source0:        http://tofrodos.sourceforge.net/download/tofrodos-%{version}.tar.gz

%description
Tofrodos is a text file conversion utility that converts ASCII and Unicode 
UTF-8 files between the MSDOS (or Windows) format, which traditionally have 
CR/LF (carriage return/line feed) pairs as their new line delimiters, and 
the Unix format, which usually have LFs (line feeds) to terminate each line.

It is a useful utility to have around when you have to convert files between 
MSDOS (or Windows) and Unix/Linux/BSD (and her clones and variants). It comes 
standard with a number of systems and is often found on the system as "todos",
"fromdos", "dos2unix" and "unix2dos".

%prep
%setup -qn tofrodos

%build
make -C src/ TFLAG="%{optflags}" LDFLAGS="%{?__global_ldflags}" %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
make -C src/ install INSTALL="install -p" BINDIR="%{buildroot}%{_bindir}" MANDIR="%{buildroot}%{_mandir}/man1/" DESTDIR=%{buildroot}

%files
%doc COPYING readme.txt tofrodos.html
%{_bindir}/fromdos
%{_bindir}/todos
%{_mandir}/man1/fromdos.1*
%{_mandir}/man1/todos.1*

%changelog
* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 1.7.13-6
- Rebuild

* Tue Oct 20 2015 Cjacker <cjacker@foxmail.com>
- Initial build.

