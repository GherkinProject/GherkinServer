#!/bin/sh
defaultStarter=/usr/local/bin/ghk-server
defaultScript=`readlink -f $defaultStarter`
dir=${defaultScript%/*}

echo "Found directory in $dir"
echo "Removing..."
if [ -d "$dir" ]
then
    rm -R $dir
    echo "Files"
fi
if [ -f "$defaultStarter" ]
then
    rm $defaultStarter
    echo "Link"
fi
echo "Done"
