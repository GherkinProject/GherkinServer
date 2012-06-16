#!/bin/sh
defaultStarter=/usr/local/bin/ghk-server
defaultScript=`readlink -f $defaultStarter`
dir=${defaultScript%/*}

echo "Found directory in $dir"

echo -n "Are you sure you want to remove this entire directory ? (y/n) "
read answer

if [ $answer = "y" ]
then
    echo "Removing..."

#All files
    if [ -d "$dir" ] || [ ! -z "$dir" ] || [ "$dir" != "${defaultScript%/*}" ]
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
else
    echo "Aborting"
fi
