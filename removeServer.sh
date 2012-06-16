#!/bin/sh
defaultStarter=/usr/local/bin/ghk-server
defaultScript=`readlink -f $defaultStarter`
dir=${defaultScript%/*}

echo "Found directory in $dir"
echo "Removing..."

#All files
if [ -d "$dir" ] || [ ! -z $dir ]
then
    rm -R $dir
    echo "Files"
fi

#Links
if [ -h "$defaultStarter" ]
then
    rm $defaultStarter
    echo "Link"
fi

echo "Done"
