#!/usr/bin/env bash

helpf()
{
    echo "migrates new dependecies with flask-sqlalchemy migrate and update commands";
    echo;
    echo "Syntax db_migrate [-m|-u|-h]";
    echo "options:-";
    echo "-m:str    message when running migrate";
    echo "-u:void   doesn't run upgrade command";
    echo "-h:void   help";
    echo;
}

# default flag values
update=1
help=0

while getopts m:u:h flag 
do
    case "${flag}" in
        m) message=${OPTARG};;
        u) update=0;;
        h) help=1;;
    esac
done

# access help
if [[ $help -eq 1 ]]
then
    helpf
    exit 0
fi

# perform commands
flask db migrate -m $message;
echo "done migration";

if [[ $update -eq 1 ]]
then
    flask db upgrade;
fi



