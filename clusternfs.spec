Summary:	ClusterNFS server
Summary(pl):	Serwer ClusterNFS
Name:		clusternfs
Version:	3.0
Release:	0.rc2.1
License:	GPL
Group:		Networking/Daemons
URL:		http://clusternfs.sourceforge.net
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}rc2.tar.bz2
Source1:	%{name}.init
Requires:	portmap >= 4.0
Provides:	nfscluster
Conflicts:	nfs-utils nfs-server
PreReq:		/sbin/chkconfig
PreReq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ClusterNFS allows diskless clients to share a single root filesystem
by matching "tagged" filenames of the form "filename$$TAG=value$$"
with fallback to the original filename.

%description -l pl
ClusterNFS pozwala bezdyskowym klientom wsp�dzieli� pojedynczy system
plik�w wybieraj�c odpowiednio "oznakowane" nazwy plik�w postaci
"plik$$TAG=warto��$$" z podmian� do oryginalnej nazwy.

%prep
%setup -q -n ClusterNFS

%build
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
./BUILD --batch \
	--rquotad=no \
	--ugidd=no --nis=yes \
	--hosts-access=yes \
	--libwrap-directory=/usr/lib \
	--exports-uid=0 --exports-gid=0 \
	--log-mounts=yes --multi=yes \
	--devtab=yes --trnames=yes \
	--path_devtab=/var/lib/clusternfs/devtab

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/adm/fillup-templates,etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/clusternfs

%post
/sbin/chkconfig --add clusternfs
if [ -r /var/lock/subsys/clusternfs ]; then
        /etc/rc.d/init.d/clusternfs restart >&2
else
        echo "Run \"/etc/rc.d/init.d/clusternfs start\" to start nfs daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -r /var/lock/subsys/clusternfs ]; then
                /etc/rc.d/init.d/clusternfs stop >&2
        fi
        /sbin/chkconfig --del clusternfs
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog* EXAMPLE.ClusterNFS HALL_OF_FAME NEWS README* TODO*
%attr(754,root,root) /etc/rc.d/init.d/clusternfs
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
/var/lib/clusternfs
