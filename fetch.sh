#!/bin/sh

mkdir -p data

curl https://api-internal.sos.ca.gov/returns/maps/president >data/president.json
for i in `seq 14 25`; do
    curl https://api-internal.sos.ca.gov/returns/maps/ballot-measures/prop/$i >data/$i.json
done
