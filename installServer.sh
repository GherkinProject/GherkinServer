#!/bin/sh
defaultDir=/usr/local/ghk-server

echo "Beginning installation of Gherkin Server"
echo -n "Default directory is $defaultDir, do you want to change it ? (y/n) "
read dirQuestion

if [ $dirQuestion = "y" ]
then
    echo "Put the absolute path where Gherkin Server will be installed (without slash at the end)"
    read dir
else
    dir=$defaultDir
fi

echo "Creating and copying files..."

#All files
if [ ! -d "$dir" ]
then
    mkdir -p $dir
    cp -R src/* $dir/
    echo "Copying files"
else
    echo "Application already installed"
fi

#Links
if [ ! -h /usr/local/bin/ghk-server ]
then
    mkdir -p /usr/local/bin
    ln -s $dir/start_server.py /usr/local/bin/ghk-server
    echo "Creating link"
else
    echo "Link already existing"
fi

echo "Done"
