%define gituser   git
Summary:	Gitolite setup used by PLD
Summary(pl.UTF-8):	Konfiguracja Gitolite wykorzystywana przez PLD
Name:		pld-gitolite
Version:	0.13.4
Release:	1.5
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/gitolite-scripts/tarball/devel/gitolite-scripts.tar.gz
# Source0-md5:	9c5c3500984e4ddb7779130ce64f57fd
Source1:	gitolite.conf
Source2:	gitolite.rc
Source3:	git.conf
Source4:	gitweb.conf
Source5:	pld-developers
Source6:	crontab
Source7:	requestrc
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	crondaemon
Requires:	git-core-slug
Requires:	gitolite
Requires:	gnupg
Requires:	perl-RPC-XML
Requires:	python3-requests
Provides:	group(%{gituser})
Provides:	user(%{gituser})
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Suggests:	git-core-daemon
Suggests:	git-core-gitweb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gitolite setup used by PLD Linux Distribution.

%description -l pl.UTF-8
Konfiguracja Gitolite wykorzystywana przez PLD.

%prep
%setup -qc
mv draenog-gitolite-scripts-*/* .

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT/home/services/%{gituser}/.gitolite/{conf,hooks/common}
install -d $RPM_BUILD_ROOT/home/services/%{gituser}/{bin,configs}

cp -p %{SOURCE1} %{SOURCE5} $RPM_BUILD_ROOT/home/services/%{gituser}/.gitolite/conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/home/services/%{gituser}/.gitolite.rc
cp -p %{SOURCE3} $RPM_BUILD_ROOT/home/services/%{gituser}/.gitconfig
cp -a hooks/* $RPM_BUILD_ROOT/home/services/%{gituser}/.gitolite/hooks/common
cp -a adc $RPM_BUILD_ROOT/home/services/%{gituser}
cp -a bin/* $RPM_BUILD_ROOT/home/services/%{gituser}/bin
cp -p %{SOURCE7} $RPM_BUILD_ROOT/home/services/%{gituser}/.requestrc

echo '*.spec' > $RPM_BUILD_ROOT/home/services/%{gituser}/configs/difforder

install -Dp %{SOURCE6} $RPM_BUILD_ROOT/etc/cron.d/git

# install additional config for gitweb package
install -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/webapps/gitweb/gitweb-pld.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 264 %{gituser}
%useradd -u 264 -d /home/services/%{gituser} -s /bin/sh -g %{gituser} -c "PLD Gitolite User" %{gituser}

%postun
if [ "$1" = "0" ]; then
	%userremove %{gituser}
	%groupremove %{gituser}
fi

%files
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/webapps/gitweb/gitweb-pld.conf
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/git

# all files owned by %{gituser}:%{gituser}
%defattr(644,%{gituser},%{gituser},755)

%dir /home/services/%{gituser}
%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/.gitconfig

%dir /home/services/%{gituser}/.gitolite
%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/.gitolite.rc

%dir /home/services/%{gituser}/.gitolite/conf
%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/.gitolite/conf/gitolite.conf
%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/.gitolite/conf/pld-developers

%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/.requestrc

%dir /home/services/%{gituser}/.gitolite/hooks
%dir /home/services/%{gituser}/.gitolite/hooks/common
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/update.secondary
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/post-receive
%dir /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/setdescription.sh
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/github.sh
/home/services/%{gituser}/.gitolite/hooks/common/post-receive.python.d
%dir /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/misc
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/misc/ciabot.pl
%dir /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/gnome
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/gnome/gnome-post-receive-email
/home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/gnome/*.py
/home/services/%{gituser}/.gitolite/hooks/common/post-receive.d/gnome-post-receive-email
%dir /home/services/%{gituser}/adc
%dir /home/services/%{gituser}/adc/bin
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/adc/bin/create
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/adc/bin/sskm
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/adc/bin/stbr
/home/services/%{gituser}/adc/bin/adc.common-functions
%dir /home/services/%{gituser}/bin
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/bin/specscommit.sh
%attr(744,%{gituser},%{gituser}) /home/services/%{gituser}/bin/pldgithub.py
%dir /home/services/%{gituser}/configs
%config(noreplace) %verify(not md5 mtime size) /home/services/%{gituser}/configs/difforder
