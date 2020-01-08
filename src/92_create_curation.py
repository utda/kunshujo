import pandas as pd
import json
import unicodedata
import collections
import requests


json_path = "data/metadata.xlsx.json"

with open(json_path) as f:
    df = json.load(f)

manifests = {}

index_map = {}

for i in range(len(df)):

    print(str(i+1)+"/"+str(len(df)))

    obj = df[i]

    id = obj["@id"]
    index = int(id.split("#")[1])

    curation_uri = obj["http://purl.org/dc/terms/relation"][0]["@id"]

    r = requests.get(curation_uri)
    data = r.json()

    member = data["selections"][0]["members"][0]

    # 不要な要素の削除

    member.pop("description")

    metadata = member["metadata"]

    indexes = []

    for j in range(len(metadata)):
        obj2 = metadata[j]
        if obj2["label"] == "タイトル" or obj2["label"] == "帖数":
            indexes.append(j)

    for j in range(len(indexes)):
        index3 = indexes[len(indexes) - j - 1]
        metadata.pop(index3)

    # ここまで

    member["label"] = obj["http://purl.org/dc/terms/title"][0]["@value"]
    member["related"] = "https://kunshujo.dl.itc.u-tokyo.ac.jp/iiif-curation-player/?curation="+curation_uri

    manifest = data["selections"][0]["within"]["@id"]

    if manifest not in index_map:

        r = requests.get(manifest)
        mani_data = r.json()

        metadata = mani_data["metadata"]

        for obj in metadata:
            if obj["label"] == "Sort":
                index2 = int(obj["value"])

                manifests[index2] = {
                    "uri": manifest,
                    "label": mani_data["label"]
                }

        index_map[manifest] = {}

    index_map[manifest][index] = member

selections = []

range = 1

for index2 in sorted(manifests):

    obj = manifests[index2]

    manifest = obj["uri"]

    tmp = index_map[manifest]

    members = []

    for index in sorted(tmp):
        members.append(tmp[index])

    selections.append({
        "@id": "https://kunshujo.dl.itc.u-tokyo.ac.jp/data/curation.json/range"+str(range),
        "@type": "sc:Range",
        "label": "Manual curation by IIIF Curation Viewer",
        "members": members,
        "within": {
            "@id": manifest,
            "label": obj["label"],
            "@type": "sc:Manifest"
        }
    })

    range += 1

result = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://kunshujo.dl.itc.u-tokyo.ac.jp/data/curation.json",
    "@type": "cr:Curation",
    "label": "電子展示『捃拾帖』",
    "selections": selections
}

with open("../docs/data/curation.json", 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
