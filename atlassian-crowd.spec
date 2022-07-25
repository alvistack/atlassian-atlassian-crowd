%global debug_package %{nil}

%global __strip /bin/true

%global __brp_mangle_shebangs /bin/true

Name: atlassian-crowd
Epoch: 100
Version: 5.0.1
Release: 1%{?dist}
Summary: Atlassian Crowd
License: Apache-2.0
URL: https://www.atlassian.com/software/crowd
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: chrpath
BuildRequires: fdupes
Requires(pre): shadow-utils
Requires: java

%description
Crowd provices single sign-on and user identity that's easy to use.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%install
install -Dpm755 -d %{buildroot}%{_unitdir}
install -Dpm755 -d %{buildroot}/opt/atlassian/crowd
cp -rfT crowd %{buildroot}/opt/atlassian/crowd
install -Dpm644 -t %{buildroot}%{_unitdir} crowd.service
chmod a+x %{buildroot}/opt/atlassian/crowd/start_crowd.sh
chmod a+x %{buildroot}/opt/atlassian/crowd/stop_crowd.sh
find %{buildroot}/opt/atlassian/crowd -type f -name '*.so' -exec chrpath -d {} \;
find %{buildroot}/opt/atlassian/crowd -type f -name '*.bak' -delete
find %{buildroot}/opt/atlassian/crowd -type f -name '*.orig' -delete
find %{buildroot}/opt/atlassian/crowd -type f -name '*.rej' -delete
fdupes -qnrps %{buildroot}/opt/atlassian/crowd

%check

%pre
set -euxo pipefail

CROWD_HOME=/var/atlassian/application-data/crowd

if [ ! -d $CROWD_HOME -a ! -L $CROWD_HOME ]; then
    mkdir -p $CROWD_HOME
fi

if ! getent group crowd >/dev/null; then
    groupadd \
        --system \
        crowd
fi

if ! getent passwd crowd >/dev/null; then
    useradd \
        --system \
        --gid crowd \
        --home-dir $CROWD_HOME \
        --no-create-home \
        --shell /usr/sbin/nologin \
        crowd
fi

chown -Rf crowd:crowd $CROWD_HOME
chmod 0750 $CROWD_HOME

%post
set -euxo pipefail

CROWD_CATALINA=/opt/atlassian/crowd

chown -Rf crowd:crowd $CROWD_CATALINA
chmod 0700 $CROWD_CATALINA

%files
%license LICENSE
%dir /opt/atlassian
%{_unitdir}/crowd.service
/opt/atlassian/crowd

%changelog
