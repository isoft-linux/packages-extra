Name:		GeoIP-GeoLite-data
# The geolite databases are updated on the first Tuesday of each month,
# hence we use a versioning scheme of YYYY.MM for the Fedora package
Version:	2015.07
Release:	1%{?dist}
Summary:	Free GeoLite IP geolocation country database
# License specified at http://dev.maxmind.com/geoip/legacy/geolite/#License
License:	CC-BY-SA
Group:		Development/Libraries
URL:		http://dev.maxmind.com/geoip/legacy/geolite/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.dat.gz
Source2:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source3:	http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz
Source4:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Source5:	http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNumv6.dat.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

%description
The GeoLite databases are free IP geolocation databases. This package contains
a database that maps IPv4 addresses to countries.

This product includes GeoLite data created by MaxMind, available from
http://www.maxmind.com/

%package extra
Summary:	Free GeoLite IP geolocation databases
Group:		Development/Libraries
License:	CC-BY-SA
Requires:	%{name} = %{version}-%{release}

%description extra
The GeoLite databases are free IP geolocation databases. This package contains
databases that map IPv6 addresses to countries, plus IPv4 and IPv6 addresses
to cities and autonomous system numbers.

This product includes GeoLite data created by MaxMind, available from
http://www.maxmind.com/

%prep
%setup -q -T -c

install -p -m 644 %{SOURCE0} GeoLiteCountry.dat.gz;	gunzip GeoLiteCountry.dat
install -p -m 644 %{SOURCE1} GeoIPv6.dat.gz;		gunzip GeoIPv6.dat
install -p -m 644 %{SOURCE2} GeoLiteCity.dat.gz;	gunzip GeoLiteCity.dat
install -p -m 644 %{SOURCE3} GeoLiteCityv6.dat.gz;	gunzip GeoLiteCityv6.dat
install -p -m 644 %{SOURCE4} GeoLiteASNum.dat.gz;	gunzip GeoLiteASNum.dat
install -p -m 644 %{SOURCE5} GeoIPASNumv6.dat.gz;	gunzip GeoIPASNumv6.dat

%build
# This section intentionally left empty

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/GeoIP/
for db in \
	GeoLiteCountry.dat \
	GeoIPv6.dat \
	GeoLiteCity.dat \
	GeoLiteCityv6.dat \
	GeoLiteASNum.dat \
	GeoIPASNumv6.dat
do
	install -p -m 644 $db %{buildroot}%{_datadir}/GeoIP/
done

# Add compat symlinks for GeoIPASNum.dat and GeoLiteASNumv6.dat
# ([upstream] database names used in the old geoip-geolite package)
ln -sf GeoLiteASNum.dat %{buildroot}%{_datadir}/GeoIP/GeoIPASNum.dat
ln -sf GeoIPASNumv6.dat %{buildroot}%{_datadir}/GeoIP/GeoLiteASNumv6.dat

# Symlinks for City databases to be where upstream expects them
# (geoiplookup -v ...)
ln -sf GeoLiteCity.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCity.dat
ln -sf GeoLiteCityv6.dat %{buildroot}%{_datadir}/GeoIP/GeoIPCityv6.dat

%clean
rm -rf %{buildroot}

%preun
# If the package is being uninstalled (rather than upgraded), we remove
# the GeoIP.dat symlink, provided that it points to GeoLiteCountry.dat;
# rpm will then be able to remove the %%{_datadir}/GeoIP directory
if [ $1 = 0 ]; then
	if [ -h %{_datadir}/GeoIP/GeoIP.dat ]; then
		geoipdat=`readlink %{_datadir}/GeoIP/GeoIP.dat`
		if [ "$geoipdat" = "GeoLiteCountry.dat" ]; then
			rm -f %{_datadir}/GeoIP/GeoIP.dat
		fi
	fi
fi
exit 0

%posttrans
# Create the default GeoIP.dat as a symlink to GeoLiteCountry.dat
#
# This has to be done in %%posttrans rather than %%post because an old
# package's GeoIP.dat may still be present during %%post in an upgrade
#
# Don't do this if there is any existing GeoIP.dat, as we don't want to
# override what the user has put there
#
# Also, if there's an existing GeoIP.dat.rpmsave, we're probably doing
# an upgrade from an old version of GeoIP that packaged GeoIP.dat as
# %%config(noreplace), so rename GeoIP.dat.rpmsave back to GeoIP.dat
# instead of creating a new symlink
if [ ! -e %{_datadir}/GeoIP/GeoIP.dat ]; then
	if [ -e %{_datadir}/GeoIP/GeoIP.dat.rpmsave ]; then
		mv %{_datadir}/GeoIP/GeoIP.dat.rpmsave \
			%{_datadir}/GeoIP/GeoIP.dat
	else
		ln -sf GeoLiteCountry.dat %{_datadir}/GeoIP/GeoIP.dat
	fi
fi
exit 0

%files
%dir %{_datadir}/GeoIP/
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCountry.dat

%files extra
# The databases are %%verify(not md5 size mtime) so that they can be updated
# via cron scripts and rpm will not moan about the files having changed
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCity.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteCityv6.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoLiteASNum.dat
%verify(not md5 size mtime) %{_datadir}/GeoIP/GeoIPASNumv6.dat
# The compat symlinks are just regular files as they should never need to be
# changed
%{_datadir}/GeoIP/GeoIPASNum.dat
%{_datadir}/GeoIP/GeoIPCity.dat
%{_datadir}/GeoIP/GeoIPCityv6.dat
%{_datadir}/GeoIP/GeoLiteASNumv6.dat

%changelog
