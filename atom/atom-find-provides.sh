#!/bin/sh
FINDPROV=/usr/lib/rpm/find-provides
$FINDPROV $* | sed -e '/libnode.so/d'
