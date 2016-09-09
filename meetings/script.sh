#!/bin/bash


conf=$1

rm db.sqlite*
rm api/migrations/0*
rm conferences/migrations/0*
rm submissions/migrations/0*
rm approvals/migrations/0*

./manage.py makemigrations
./manage.py migrate
if [[ -n "$conf" ]]; then
	./manage.py loadtestdata conferences.Conference:${conf}
else 
	echo "creating empty database"
fi
./manage.py runserver
