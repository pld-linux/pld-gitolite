Summary:	Gitolite setup used by PLD
Name:		pld-gitolite
Version:	0.2
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/gitolite-scripts/tarball/v%{version}/gitolite-scripts.tar.gz
# Source0-md5:	5b22b8bb558261367ed18028934afb6a
Source1:	gitolite.conf
Source2:	gitolite.rc
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	gitolite
Provides:	group(gitolite)
Provides:	user(gitolite)
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
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
cp -a hooks/* $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/hooks/common
cp -a adc $RPM_BUILD_ROOT/home/services/gitolite/


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

# all files owned by gitolite:gitolite
%defattr(644,gitolite,gitolite,755)

%dir /home/services/gitolite
%dir /home/services/gitolite/repositories

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
/home/services/gitolite/.gitolite/hooks/common/post-receive.python.d
%dir /home/services/gitolite/adc
%dir /home/services/gitolite/adc/bin
%attr(744,gitolite,gitolite) /home/services/gitolite/adc/bin/create
/home/services/gitolite/adc/bin/adc.common-functions
