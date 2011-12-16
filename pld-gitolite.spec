Summary:	Gitolite setup used by PLD
Name:		pld-gitolite
Version:	0.1
Release:	0.1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/gitolite-scripts/tarball/v%{version}/gitolite-scripts.tar.bz2
# Source0-md5:	ac759e1ab4d95fd154a30c3c5254de40
Source1:	gitolite.conf
Source2:	gitolite.rc
Requires:	gitolite
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gitolite setup used by PLD Linux Distribution

%prep
%setup -qc
mv draenog-gitolite-scripts-*/* .

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/home/services/gitolite/repositories
install -d $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/{conf,hooks/common}

cp -a %{SOURCE1} $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT/home/services/gitolite/.gitolite.rc
cp -a hooks/* $RPM_BUILD_ROOT/home/services/gitolite/.gitolite/hooks/common
cp -a adc $RPM_BUILD_ROOT/home/services/gitolite/
touch $RPM_BUILD_ROOT/home/services/gitolite//projects.list


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 264 gitolite
%useradd -u 264 -d /home/services/gitolite -s /bin/sh -g gitolite -c "PLD Gitolie User" gitolite

%post

%preun

%postun
if [ "$1" = "0" ]; then
	%userremove gitolite
	%groupremove gitolite
fi


%files
%defattr(644,gitolite,gitolite,755)
/home/services/gitolite
%dir /home/services/gitolite/repositories
%config(noreplace) %verify(not md5 mtime size) /home/services/gitolite/.gitolite/conf/gitolite.conf
%config(noreplace) %verify(not md5 mtime size) /home/services/gitolite/.gitolite.rc
%attr(744,gitolite,gitolite) /home/services/gitolite/adc/bin/create
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common//update.secondary
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common//post-receive
%attr(744,gitolite,gitolite) /home/services/gitolite/.gitolite/hooks/common//post-receive.d/mailnotification
