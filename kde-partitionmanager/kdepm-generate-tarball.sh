#!/bin/sh

if [ $# -ne 1 ]
then
  echo Usage : ./kdepm-generate-tarball.sh SVN_DATE
  exit 1
fi

NAME_VERSION=kde-partitionmanager-1.0.3
SVN_DATE=$1

# Remove old sources if exist
rm -R --force ${NAME_VERSION}

# Checkout svn trunk
svn -r {${SVN_DATE}} export svn://anonsvn.kde.org/home/kde/trunk/extragear/sysadmin/partitionmanager/ ${NAME_VERSION}

# Create source tarball
tar cJvf ${NAME_VERSION}-${SVN_DATE}svn.tar.xz ${NAME_VERSION}

# Delete temporary directories
rm -R --force ${NAME_VERSION}
