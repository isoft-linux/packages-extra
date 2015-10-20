#!/bin/sh
FINDREQ=/usr/lib/rpm/find-requires
$FINDREQ $* | sed -e '/libnode.so/d'
