# -*- coding: utf-8 -*-
import json
import csv

import glob

def rep(json_str, map):
    for key in map:
        org = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+key+"/canvas/"
        aft = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+map[key]+"/canvas/"
        json_str = json_str.replace(org, aft)

        org = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+key+"/manifest"
        aft = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+map[key]+"/manifest"
        json_str = json_str.replace(org, aft)
    return json_str


files = glob.glob("../docs/data/curation/*.json")

f = open('data/replace_id_list.csv', 'r')

map = dict()

reader = csv.reader(f)
header = next(reader)
for row in reader:
    map[row[0]] = row[1]

f.close()

for file in files:

    with open(file) as json_data:
        data = json.load(json_data)

    json_str = json.dumps(data)

    json_str = rep(json_str, map)

    data = json.loads(json_str)

    with open(file, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
