Summary:	ClusterNFS server
Summary(pl):	Serwer ClusterNFS
Name:		clusternfs
Version:	3.0.rc2
Release:	1
License:	GPL
Group:		Networking/Daemons
URL:		http://clusternfs.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	clusternfs.init
Requires:	portmap >= 4.0
Provides:	nfscluster
Conflicts:	nfs-utils nfs-server
PreReq:		/sbin/chkconfig
PreReq:		rc-scripts
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
ClusterNFS allows diskless clients to share a single root filesystem
by matching "tagged" filenames of the form "filename$$TAG=value$$" 
with fallback to the original filename.

%description -l pl
ClusterNFS pozwala bezdyskowym klientom wspó³dzieliæ pojedynczy system 
plików wybieraj±c odpowiednio "oznakowane" nazwy plików postaci 
"plik$$TAG=warto¶æ$$" z podmian± do oryginalnej nazwy.

%prep
rm -fr %{buildroot}
%setup -q

%build
./BUILD --batch \
	--rquotad=no \
	--ugidd=no --nis=yes \
	--hosts-access=yes\
	--libwrap-directory=%{_libdir} \
	--exports-uid=0 --exports-gid=0 \
	--log-mounts=yes --multi=yes \
	--devtab=yes --trnames=yes \
	--path_devtab=%{_localstatedir}/nfs/devtab

make

%install
rm -fr %{buildroot}

make DESTDIR=%{buildroot} install
install -d %{buildroot}/var/adm/fillup-templates %{buildroot}/etc/rc.d/init.d
install -m 755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/clusternfs

%post

/sbin/chkconfig --add clusternfs
if [ -r /var/lock/subsys/clusternfs ]; then
        /etc/rc.d/init.d/clusternfs restart >&2
else
        echo "Run \"/etc/rc.d/init.d/clusternfs start\" to start nfs daemon."
fi
#sed -e 's/NFSDTYPE=.*/NFSDTYPE=K/' /etc/sysconfig/nfsd > /etc/sysconfig/nfsd.new
#mv -f /etc/sysconfig/nfsd.new /etc/sysconfig/nfsd

%preun
if [ "$1" = "0" ]; then
        if [ -r /var/lock/subsys/clusternfs ]; then
                /etc/rc.d/init.d/clusternfs stop >&2
        fi
        /sbin/chkconfig --del clusternfs
fi
					
%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS COPYING ChangeLog HALL_OF_FAME NEWS README README.HISTORIC TODO README.ClusterNFS EXAMPLE.ClusterNFS
%{_mandir}/man5/*
%{_mandir}/man8/[m-r]*
%{_localstatedir}/nfs
%{_sbindir}/rpc.*
%config(noreplace) %{_initrddir}/clusternfs

%changelog
