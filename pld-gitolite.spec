# TODO:
# - real webapps integration
Summary:	Gitolite setup used by PLD
Name:		pld-gitolite
Version:	0.6
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/gitolite-scripts/tarball/v%{version}/gitolite-scripts.tar.gz
# Source0-md5:	bf460d4f33c346a7276f996a2859ddf0
Source1:	gitolite.conf
Source2:	gitolite.rc
Source3:	git.conf
Source4:	gitweb.conf
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	gitolite
Requires:	perl-RPC-XML
Provides:	group(gitolite)
Provides:	user(gitolite)
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
Gitolite setup used by PLD Linux Distribution

%prep
%setup -qc
mv draenog-gitolite-scripts-*/* .

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT/home/services/gitolite/repositories
install -d $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/{conf,hooks/common}

cp -p %{SOURCE1} $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/home/services/gitolite/.gitolite.rc
cp -p %{SOURCE3} $RPM_BUILD_ROOT/home/services/gitolite/.gitconfig
cp -a hooks/* $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/hooks/common
cp -a adc $RPM_BUILD_ROOT/home/services/gitolite

install -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/webapps/gitweb/gitweb-pld.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 264 gitolite
%useradd -u 264 -d /home/services/gitolite -s /bin/sh -g gitolite -c "PLD Gitolite User" gitolite

%postun
if [ "$1" = "0" ]; then
	%userremove gitolite
	%groupremove gitolite
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/webapps/gitweb/gitweb-pld.conf

# all files owned by gitolite:gitolite
%defattr(644,gitolite,gitolite,755)

%dir /home/services/gitolite
%dir /home/services/gitolite/repositories
%config(noreplace) %verify(not md5 mtime size) /home/services/gitolite/.gitconfig

%dir /home/services/gitolite/.gitolite
%config(noreplace) %verify(not md5 mtime size) /home/services/gitolite/.gitolite.rc

%dir /home/services/gitolite/.gitolite/conf
%config(noreplace) %verify(not md5 mtime size) /home/services/gitolite/.gitolite/conf/gitolite.conf

%dir /home/services/gitolite/.gitolite/hooks
%dir /home/services/gitolite/.gitolite/hooks/common
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common/update.secondary
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common/post-receive
%dir /home/services/gitolite/.gitolite/hooks/common/post-receive.d
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common/post-receive.d/mailnotification
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common/post-receive.d/setdescription.sh
/home/services/gitolite/.gitolite/hooks/common/post-receive.python.d
%dir /home/services/gitolite/.gitolite/hooks/common/post-receive.d/misc
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common/post-receive.d/misc/ciabot.pl
%dir /home/services/gitolite/adc
%dir /home/services/gitolite/adc/bin
%attr(744,gitolite,gitolite) /home/services/gitolite/adc/bin/create
/home/services/gitolite/adc/bin/adc.common-functions
