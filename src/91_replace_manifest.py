# -*- coding: utf-8 -*-
import json
import csv

import glob


files = glob.glob("../docs/data/curation/*.json")

for file in files:

    with open(file) as json_data:
        data = json.load(json_data)

    manifest = data["selections"][0]["within"]["@id"]
    uuid = manifest.split("/")[-2]
    manifest = "https://archdataset.dl.itc.u-tokyo.ac.jp/manifest/"+uuid+".json"
    data["selections"][0]["within"]["@id"] = manifest

    with open(file, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
