#!/usr/bin/env python3
import csv
import json
import os


def load():
    ret = {}
    for filename in os.listdir('data'):
        with open(f'data/{filename}') as f:
            ret[os.path.splitext(filename)[0]] = json.load(f)
    return ret


def _int(num):
    return int(num.replace(',', ''))


def transform(data):
    ret = {}
    for race, race_data in data.items():
        for county, county_data in race_data.items():
            if race == 'president':
                for candidate in county_data['candidates']:
                    if 'Biden' in candidate['Name']:
                        biden = _int(candidate['Votes'])
                    elif 'Trump' in candidate['Name']:
                        trump = _int(candidate['Votes'])

                ret[(race, county)] = biden / (biden + trump)
            else:
                measure = county_data['ballot-measures'][0]
                yes = _int(measure['yesVotes'])
                no = _int(measure['noVotes'])
                ret[(race, county)] = yes / (yes + no)
    return ret


def dump(data):
    races = list(sorted(set(r for r, c in data)))
    counties = list(sorted(set(c for r, c in data)))
    with open('data/out.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow([''] + races)
        for c in counties:
            w.writerow([c] + [data[(r, c)] for r in races])


if __name__ == '__main__':
    dump(transform(load()))
