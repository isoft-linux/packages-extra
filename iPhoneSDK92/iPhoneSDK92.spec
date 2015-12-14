#disable strip
%define __spec_install_post /usr/lib/rpm/brp-compress || :

Name: iPhoneSDK92
Version: 9.2
Release: 2
Summary: iPhoneOS9.2.sdk exported from Xcode

License: Commercial
URL: http://www.apple.com

#mkdir ~/xcode
#darling-dmg Xcode_7.2.dmg ~/xcode
#mkdir -p iPhoneOS9.2.sdk
#cp -r xcode/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/* iPhoneOS9.2.sdk
#cp -r xcode/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/* iPhoneOS9.2.sdk/usr/include/c++
#mkdir -p iPhoneOS9.2.sdk/usr/lib/arc
#cp -r xcode/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/arc/libarclite_iphoneos.a iPhoneOS9.2.sdk/usr/lib/arc
Source0: iPhoneOS9.2.sdk.tar.xz

AutoReqProv: no

%description
%{summary}

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}
tar Jxf %{SOURCE0} -C %{buildroot}%{_datadir}

%files
%dir %{_datadir}/iPhoneOS%{version}.sdk
%{_datadir}/iPhoneOS%{version}.sdk/*

%changelog
* Sun Dec 13 2015 Cjacker <cjacker@foxmail.com> - 9.2-2
- Initial build


