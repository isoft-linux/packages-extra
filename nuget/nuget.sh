#!/bin/sh
MONO_PATH=/usr/lib/nuget:$MONO_PATH
export MONO_PATH
exec mono $MONO_OPTIONS /usr/lib/nuget/NuGet.exe "$@"
