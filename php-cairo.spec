%define rname Cairo
%define modname cairo
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A98_%{modname}.ini

Summary:	Cairo Graphics Library Extension
Name:		php-%{modname}
Version:	0.1.0
Release:	%mkrel 3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/Cairo/
Source0:	http://pecl.php.net/get/%{rname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	pkgconfig
BuildRequires:	cairo-devel >= 1.4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot} 

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

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS IGNORED README SYMBOLS TODO package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

