import pandas as pd
import json
import unicodedata
import collections


def form(data):
    return unicodedata.normalize("NFKC", data)


json_path = "data/metadata.xlsx.json"

with open(json_path) as f:
    df = json.load(f)

result = []

dcterms = "http://purl.org/dc/terms/"
archiveshub = "http://data.archiveshub.ac.uk/def/"
bibo = "http://purl.org/ontology/bibo/"

# 表示用項目
label_map = collections.OrderedDict()
label_map["表題"] = dcterms + "title"
label_map["帖数"] = bibo + "volume"
label_map["目録番号"] = dcterms + "identifier"
label_map["書誌事項"] = dcterms + "description"
label_map["数量"] = dcterms + "extent"
label_map["和暦"] = archiveshub + "dateCreatedAccumulatedString"
label_map["西暦コード"] = archiveshub + "dateCreatedAccumulated"
label_map["地名"] = dcterms + "coverage"
label_map["版種類"] = dcterms + "type"
label_map["形態分類"] = dcterms + "format"
label_map["内容分類"] = dcterms + "subject"
label_map["URL"] = dcterms + "relation"

row_map = dict()

for i in range(len(df)):
    obj = df[i]

    row = []
    for key in label_map:
        text = ""

        e = label_map[key]

        if e in obj:
            tmp = obj[e]
            for j in range(len(tmp)):
                if e == bibo + "volume":
                    text += "『捃拾帖』第" + str(tmp[j]["@value"]) + "帖"
                elif e == dcterms + "relation":
                    text += "https://kunshujo.dl.itc.u-tokyo.ac.jp/iiif-curation-player/?curation=" + str(tmp[j]["@id"])
                else:
                    text += str(tmp[j]["@value"])

                if j != len(tmp) - 1:
                    text += "・"

            if e == dcterms + "identifier":
                id = tmp[0]["@value"]
                ids = id.split("-")
                id = ids[3].zfill(4) + "-" + ids[4].zfill(4)
                row_map[id] = row

        row.append(form(text))

row = []
for key in label_map:
    row.append(key)
result.append(row)

for key in sorted(row_map):
    result.append(row_map[key])

df = pd.DataFrame(result)

df.to_excel("../docs/data/metadata.xlsx", index=False, header=False)
