# -*- coding: utf-8 -*-
import urllib.request, json
from bs4 import BeautifulSoup

endpoint = "https://diyhistory.org/public/omekac/api"


def exec2collection(org_canvas, org_label, org_manifest):
    flg = True
    page = 1

    members = {}

    while flg:
        url = endpoint + "/items?item_type=18&search=" + org_canvas + "&page=" + str(page)
        print(url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):

                # 各アイテム
                obj = data[i]

                modified = obj["modified"].split("T")[0]

                element_texts = obj["element_texts"]
                for e in element_texts:

                    if e["element"]["name"] == "Text":
                        text = BeautifulSoup(e["text"], "lxml").text
                        es = text.split("-")

                        id = es[3]

                        if id not in hist:
                            hist[id] = 0
                        hist[id] = hist[id] + 1

                        break

                if modified not in all:
                    all[modified] = 0
                all[modified] = all[modified] + 1

        else:
            flg = False


cflg = True
cpage = 1

all = {}
hist = {}

while cflg:
    curl = endpoint + "/collections?page=" + str(cpage)
    print(curl)

    cpage += 1

    cresponse = urllib.request.urlopen(curl)
    cresponse_body = cresponse.read().decode("utf-8")
    cdata = json.loads(cresponse_body.split('\n')[0])

    if len(cdata) > 0:
        for i in range(len(cdata)):
            # 各アイテム
            obj = cdata[i]

            org_label = ""
            org_canvas = ""
            org_manifest = ""

            element_texts = obj["element_texts"]
            for e in element_texts:

                if e["element"]["id"] == 50:
                    org_label = e["text"]
                elif e["element"]["id"] == 48:
                    org_manifest = e["text"]
                    org_canvas = org_manifest.replace("manifest", "canvas")

            exec2collection(org_canvas, org_label, org_manifest)

    else:
        cflg = False

data_dir = "data"

with open(data_dir + "/rows.json") as json_data:
    rows = json.load(json_data)

hist["1"] = 270
all["2018-10-23"] = 270

result = {}
result["progress"] = all
result["hist"] = hist
result["rows"] = rows

with open("../../docs/data/progress.json", 'w') as outfile:
    json.dump(result, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
