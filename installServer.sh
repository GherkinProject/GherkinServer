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

echo "Creating and copying files"
mkdir $dir
cp -R src/* $dir/
chown -R $USER $dir
ln -s $dir/start_server.py /usr/local/bin/ghk-server
