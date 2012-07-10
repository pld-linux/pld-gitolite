# TODO:
# - real webapps integration

%define gituser   git

Summary:	Gitolite setup used by PLD
Name:		pld-gitolite
Version:	0.11
Release:	0.1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/gitolite-scripts/tarball/v%{version}/gitolite-scripts.tar.gz
# Source0-md5:	44f58773a1353c7a78b2627bee082377
Source1:	gitolite.conf
Source2:	gitolite.rc
Source3:	git.conf
Source4:	gitweb.conf
Source5:	pld-developers
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	git-core-slug
Requires:	gitolite
Requires:	perl-RPC-XML
Provides:	group(%gituser)
Provides:	user(%gituser)
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

%prep
%setup -qc
mv draenog-gitolite-scripts-*/* .

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT/home/services/%gituser/.gitolite/{conf,hooks/common}

cp -p %{SOURCE1} %{SOURCE5} $RPM_BUILD_ROOT/home/services/%gituser/.gitolite/conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/home/services/%gituser/.gitolite.rc
cp -p %{SOURCE3} $RPM_BUILD_ROOT/home/services/%gituser/.gitconfig
cp -a hooks/* $RPM_BUILD_ROOT/home/services/%gituser/.gitolite/hooks/common
cp -a adc $RPM_BUILD_ROOT/home/services/%gituser

install -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/webapps/gitweb/gitweb-pld.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 264 %gituser
%useradd -u 264 -d /home/services/%gituser -s /bin/sh -g %gituser -c "PLD Gitolite User" %gituser

%postun
if [ "$1" = "0" ]; then
	%userremove %gituser
	%groupremove %gituser
fi

%files
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/webapps/gitweb/gitweb-pld.conf

# all files owned by %gituser:%gituser
%defattr(644,%gituser,%gituser,755)

%dir /home/services/%gituser
%config(noreplace) %verify(not md5 mtime size) /home/services/%gituser/.gitconfig

%dir /home/services/%gituser/.gitolite
%config(noreplace) %verify(not md5 mtime size) /home/services/%gituser/.gitolite.rc

%dir /home/services/%gituser/.gitolite/conf
%config(noreplace) %verify(not md5 mtime size) /home/services/%gituser/.gitolite/conf/gitolite.conf
%config(noreplace) %verify(not md5 mtime size) /home/services/%gituser/.gitolite/conf/pld-developers

%dir /home/services/%gituser/.gitolite/hooks
%dir /home/services/%gituser/.gitolite/hooks/common
%attr(744,%gituser,%gituser) /home/services/%gituser/.gitolite/hooks/common/update.secondary
%attr(744,%gituser,%gituser) /home/services/%gituser/.gitolite/hooks/common/post-receive
%dir /home/services/%gituser/.gitolite/hooks/common/post-receive.d
%attr(744,%gituser,%gituser) /home/services/%gituser/.gitolite/hooks/common/post-receive.d/setdescription.sh
/home/services/%gituser/.gitolite/hooks/common/post-receive.python.d
%dir /home/services/%gituser/.gitolite/hooks/common/post-receive.d/misc
%attr(744,%gituser,%gituser) /home/services/%gituser/.gitolite/hooks/common/post-receive.d/misc/ciabot.pl
%dir /home/services/%gituser/.gitolite/hooks/common/post-receive.d/gnome
%attr(744,%gituser,%gituser) /home/services/%gituser/.gitolite/hooks/common/post-receive.d/gnome/gnome-post-receive-email
/home/services/%gituser/.gitolite/hooks/common/post-receive.d/gnome/*.py
/home/services/%gituser/.gitolite/hooks/common/post-receive.d/gnome-post-receive-email
%dir /home/services/%gituser/adc
%dir /home/services/%gituser/adc/bin
%attr(744,%gituser,%gituser) /home/services/%gituser/adc/bin/create
%attr(744,%gituser,%gituser) /home/services/%gituser/adc/bin/sskm
/home/services/%gituser/adc/bin/adc.common-functions
