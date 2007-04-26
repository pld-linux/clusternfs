Summary:	ClusterNFS server
Summary(pl.UTF-8):	Serwer ClusterNFS
Name:		clusternfs
Version:	3.0
Release:	0.rc2.2
License:	GPL v2
Group:		Networking/Daemons
URL:		http://clusternfs.sourceforge.net/
Source0:	http://dl.sourceforge.net/clusternfs/%{name}-%{version}rc2.tar.bz2
# Source0-md5:	b25b578b2dd3222b554c4953a32efc8f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-types.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	portmap >= 4.0
Requires:	rc-scripts >= 0.4.1.5
Provides:	nfscluster
Conflicts:	nfs-server
Conflicts:	nfs-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ClusterNFS allows diskless clients to share a single root filesystem
by matching "tagged" filenames of the form "filename$$TAG=value$$"
with fallback to the original filename.

%description -l pl.UTF-8
ClusterNFS pozwala bezdyskowym klientom współdzielić pojedynczy system
plików wybierając odpowiednio "oznakowane" nazwy plików postaci
"plik$$TAG=wartość$$" z podmianą do oryginalnej nazwy.

%prep
%setup -q -n ClusterNFS
%patch0 -p1

%build
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
./BUILD --batch \
	--rquotad=no \
	--ugidd=no --nis=yes \
	--hosts-access=yes \
	--libwrap-directory=%{_prefix}/lib \
	--exports-uid=0 --exports-gid=0 \
	--log-mounts=yes --multi=yes \
	--devtab=yes --trnames=yes \
	--path_devtab=/var/lib/clusternfs/devtab

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/clusternfs
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/clusternfs
> $RPM_BUILD_ROOT%{_sysconfdir}/exports

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add clusternfs
%service clusternfs restart "NFS daemon"

%preun
if [ "$1" = "0" ]; then
	%service clusternfs stop
	/sbin/chkconfig --del clusternfs
fi

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog* EXAMPLE.ClusterNFS HALL_OF_FAME NEWS README* TODO*
%attr(754,root,root) /etc/rc.d/init.d/clusternfs
%attr(755,root,root) %{_sbindir}/rpc.*
%{_mandir}/man5/*
%{_mandir}/man8/[mn]*
%attr(664,root,fileshare) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/exports
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/clusternfs
/var/lib/clusternfs
