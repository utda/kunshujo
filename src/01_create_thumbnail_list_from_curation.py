# -*- coding: utf-8 -*-
import json
import csv

import glob

files = glob.glob("../docs/data/curation/*")

table = []

for file in files:

    with open(file) as json_data:
        data = json.load(json_data)

    selections = data["selections"]

    selection = selections[0]

    members = selection["members"]

    manifest = selection["within"]["@id"]

    for i in range(len(members)):

        obj = members[i]
        label = obj["label"]

        if "thumbnail" in obj:
            thumb = obj["thumbnail"]

            row = [label, thumb]
            table.append(row)

with open('data/thumbnail_list.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
    writer.writerows(table)  # 2次元配列も書き込める
