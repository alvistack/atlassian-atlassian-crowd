#!/bin/bash

CROWD_HOME="/var/atlassian/application-data/crowd"
CROWD_CATALINA="/opt/atlassian/crowd"

JAVA_OPTS="-Dfile.encoding=UTF-8 ${JAVA_OPTS}"
JAVA_OPTS="-Xms2048m -Xmx2048m -XX:ReservedCodeCacheSize=512m ${JAVA_OPTS}"
JAVA_OPTS="-Datlassian.plugins.enable.wait=300 -XX:+UnlockExperimentalVMOptions ${JAVA_OPTS}"
export JAVA_OPTS

CATALINA_OPTS="-Dcrowd.home=$CROWD_HOME ${CATALINA_OPTS}"
CATALINA_OPTS="-XX:+UseZGC -XX:+ExplicitGCInvokesConcurrent ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.connector.port=8095 ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.connector.scheme=http ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.connector.secure=false ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.connector.proxyname= ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.connector.proxyport= ${CATALINA_OPTS}"
CATALINA_OPTS="-Dcrowd.catalina.context.path= ${CATALINA_OPTS}"
export CATALINA_OPTS

# set the location of the pid file
if [ -z "$CATALINA_PID" ] ; then
    if [ -n "$CATALINA_BASE" ] ; then
        CATALINA_PID="$CATALINA_BASE"/work/catalina.pid
    elif [ -n "$CATALINA_HOME" ] ; then
        CATALINA_PID="$CATALINA_HOME"/work/catalina.pid
    fi
fi
export CATALINA_PID
