#!/bin/sh
echo -n "Do you really want to delete config files of Gherkin Server ? (y/n)"
read answer

if [ $answer = "y" ]
then
    rm -f ~/.ghk/db.xml ~/.ghk/configServer.cfg ~/.ghk/dbMarkov.ghk ~/.ghk/server.log
    echo "Done"
else
    echo "Aborting"
fi
