%define rname Cairo
%define modname cairo
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A98_%{modname}.ini

Summary:	Cairo Graphics Library Extension
Name:		php-%{modname}
Version:	0.3.2
Release:	4
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/Cairo/
Source0:	http://pecl.php.net/get/%{rname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	pkgconfig
BuildRequires:	cairo-devel >= 1.4

%description
Cairo is a 2D graphics library with support for multiple output devices.
Currently supported output targets include the X Window System, Quartz, Win32,
image buffers, PostScript, PDF, and SVG file output.

%prep

%setup -q -n %{rname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files 
%doc CREDITS IGNORED README SYMBOLS TODO package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.3.2-2mdv2012.0
+ Revision: 795406
- rebuild for php-5.4.x

* Mon Apr 23 2012 Oden Eriksson <oeriksson@mandriva.com> 0.3.2-1
+ Revision: 792792
- 0.3.2

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-1
+ Revision: 790145
- 0.3.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-10
+ Revision: 761205
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-9
+ Revision: 696398
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-8
+ Revision: 695371
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-7
+ Revision: 646617
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-6mdv2011.0
+ Revision: 629770
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-5mdv2011.0
+ Revision: 628072
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-4mdv2011.0
+ Revision: 600466
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-3mdv2011.0
+ Revision: 588748
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-2mdv2010.1
+ Revision: 514522
- rebuilt for php-5.3.2

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2010.1
+ Revision: 506531
- 0.2.0

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2010.1
+ Revision: 485344
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2010.1
+ Revision: 468149
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.0
+ Revision: 452904
- import php-cairo


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2010.0
- initial Mandriva package
