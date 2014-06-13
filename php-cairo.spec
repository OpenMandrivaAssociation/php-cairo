%define rname Cairo
%define modname cairo
%define soname %{modname}.so
%define inifile A98_%{modname}.ini

Summary:	Cairo Graphics Library Extension
Name:		php-%{modname}
Version:	0.3.2
Release:	8
Group:		Development/PHP
License:	PHP License
Url:		http://pecl.php.net/package/Cairo/
Source0:	http://pecl.php.net/get/%{rname}-%{version}.tgz
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pkgconfig(cairo)

%description
Cairo is a 2D graphics library with support for multiple output devices.
Currently supported output targets include the X Window System, Quartz, Win32,
image buffers, PostScript, PDF, and SVG file output.

%prep

%setup -qn %{rname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

phpize
%configure2_5x \
	--with-libdir=%{_lib} \
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

