# Copyright 2023 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global __strip /bin/true

%global __brp_mangle_shebangs /bin/true

Name: atlassian-crowd
Epoch: 100
Version: 5.0.3
Release: 1%{?dist}
Summary: Atlassian Crowd
License: Apache-2.0
URL: https://www.atlassian.com/software/crowd
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: -post-build-checks
Requires(pre): chrpath
Requires(pre): fdupes
Requires(pre): patch
Requires(pre): shadow-utils
Requires(pre): wget

%description
Crowd provices single sign-on and user identity that's easy to use.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%install
install -Dpm755 -d %{buildroot}%{_unitdir}
install -Dpm755 -d %{buildroot}/opt/atlassian/crowd
install -Dpm644 -t %{buildroot}%{_unitdir} crowd.service
install -Dpm644 -t %{buildroot}/opt/atlassian atlassian-crowd.patch

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

CROWD_DOWNLOAD_URL=http://product-downloads.atlassian.com/software/crowd/downloads/atlassian-crowd-5.0.3
tar.gz
CROWD_DOWNLOAD_DEST=/tmp/atlassian-crowd-5.0.3.tar.gz
CROWD_DOWNLOAD_CHECKSUM=c78751e3324e30a7168c9dbaadb2f0207b9fd9207a09cde36e8f996e8fa08884

CROWD_PATCH=/opt/atlassian/atlassian-crowd.patch
CROWD_CATALINA=/opt/atlassian/crowd

wget -c $CROWD_DOWNLOAD_URL -O $CROWD_DOWNLOAD_DEST
echo -n "$CROWD_DOWNLOAD_CHECKSUM $CROWD_DOWNLOAD_DEST" | sha256sum -c -
rm -rf $CROWD_CATALINA

mkdir -p $CROWD_CATALINA
tar zxf $CROWD_DOWNLOAD_DEST -C $CROWD_CATALINA --strip-components=1

cat $CROWD_PATCH | patch -p1 -d /
chmod a+x $CROWD_CATALINA/start_crowd.sh
chmod a+x $CROWD_CATALINA/stop_crowd.sh
find $CROWD_CATALINA -type f -name '*.so' -exec chrpath -d {} \;
find $CROWD_CATALINA -type f -name '*.bak' -delete
find $CROWD_CATALINA -type f -name '*.orig' -delete
find $CROWD_CATALINA -type f -name '*.rej' -delete
fdupes -qnrps $CROWD_CATALINA

chown -Rf crowd:crowd $CROWD_CATALINA
chmod 0700 $CROWD_CATALINA

%files
%license LICENSE
%dir /opt/atlassian
%dir /opt/atlassian/crowd
%{_unitdir}/crowd.service
/opt/atlassian//atlassian-crowd.patch

%changelog
