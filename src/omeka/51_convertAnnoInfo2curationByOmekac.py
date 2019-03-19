# -*- coding: utf-8 -*-
import urllib.request, json
from bs4 import BeautifulSoup
from hashlib import md5
import pandas as pd


def make_md5(s):
    return md5(s.encode('utf-8')).hexdigest()


def get_list(path):
    df = pd.read_excel(path)

    data = {}

    for index, row in df.iterrows():
        id = row["12目録番号"]
        meta = {}
        data[id] = meta
        meta["和暦"] = row["和暦"]
        meta["西暦コード"] = row["3西暦コード"]
        meta["タイトル"] = row["タイトル"]
        meta["版種類"] = row["5版種類"]
        meta["数量"] = row["数量"]
        meta["書誌事項"] = row["7書誌事項"]
        meta["形態分類"] = row["形態分類"]
        meta["内容分類"] = row["9内容分類"]
        meta["帖数"] = row["volume"]
        meta["地名"] = row["地名"]

    return data


def getInfoFromManifest(url, collection_manifest, members):
    response = urllib.request.urlopen(url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    anno_list_url = data["sequences"][0]["canvases"][0]["otherContent"][0]["@id"];

    image_url = data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"];

    response = urllib.request.urlopen(anno_list_url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    resources = data["resources"]

    for i in range(len(resources)):
        resource = resources[i]
        text = resource["resource"][0]["chars"]
        text = BeautifulSoup(text, "lxml").text

        o_name = text

        selector = resource["on"][0]["selector"]["default"]["value"]

        canvas_id = resource["on"][0]["full"]

        tmp = o_name.split("-")
        if len(tmp) == 6:
            o_name = tmp[0] + "-" + tmp[1] + "-" + tmp[2] + "-" + tmp[3] + "-" + tmp[4] + "_" + tmp[5]

        o_name = o_name.split("_")[0]

        n = o_name.split("-")[4]
        if not n.isdigit():
            print(text)
            continue

        if o_name not in members:
            members[o_name] = {}

        tmp = {}
        members[o_name][int(canvas_id.split("canvas/p")[1])] = tmp
        tmp["selection"] = canvas_id + "#" + selector
        tmp["label"] = o_name

        tmp["thumbnail"] = image_url + "/" + selector.split("=")[1] + "/,300/0/default.jpg"


uuid_map = {}
manifests = []


def exec2collection(org_canvas, org_label, org_manifest):
    flg = True
    page = 1

    members = {}

    while flg:
        url = endpoint + "/items?item_type=18&search=" + org_canvas + "&page=" + str(page)
        print("url:\t" + url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):

                if i % 10 == 0:
                    print(i)

                # 各アイテム
                obj = data[i]

                element_texts = obj["element_texts"]
                for e in element_texts:

                    if e["element"]["name"] == "On Canvas":
                        uuid = e["text"]

                        if uuid not in uuid_map:
                            tmp_url = endpoint + "/items?search=" + uuid

                            # print("tmp_url:\t" + tmp_url)

                            response = urllib.request.urlopen(tmp_url)
                            response_body = response.read().decode("utf-8")
                            data_t = json.loads(response_body.split('\n')[0])

                            uuid_map[uuid] = data_t[0]

                        obj_t = uuid_map[uuid]

                        id = obj_t["id"]
                        collection_id = obj_t["collection"]["id"]

                manifest = endpoint.replace("/api", "") + "/oa/items/" + str(id) + "/manifest.json"

                collection_manifest = endpoint.replace("/api", "") + "/oa/collections/" + str(
                    collection_id) + "/manifest.json"

                if manifest not in manifests:
                    getInfoFromManifest(manifest, collection_manifest, members)
                    manifests.append(manifest)

        else:
            flg = False

    # print(members)

    for o_name in members:

        # print("***\t"+o_name)

        with open(data_dir + '/template.json') as f:
            df = json.load(f)

        df["selections"] = []

        selection = {}
        df["selections"].append(selection)

        df["@id"] = "https://kunshujo.dl.itc.u-tokyo.ac.jp/data/curation/" + o_name + ".json"
        selection["@id"] = df["@id"] + "/range" + str(1)

        selection["@type"] = "sc:Range"
        selection["label"] = "Manual curation by IIIF Curation Viewer"

        selection["members"] = []

        manifest = {}
        selection["within"] = manifest
        manifest["@id"] = org_manifest
        manifest["@type"] = "sc:Manifest"
        manifest["@label"] = org_label

        count = 1

        for canvas in sorted(members[o_name]):

            member = {}

            selection["members"].append(member)

            tmp = members[o_name][canvas]

            member["@id"] = tmp["selection"]
            member["@type"] = "sc:Canvas"
            member["label"] = tmp["label"]
            member["thumbnail"] = tmp["thumbnail"]

            meta = list[member["label"]]

            metadata = []
            member["metadata"] = metadata

            description = "<table class=\"table\">"

            for key in meta:
                if meta[key] != "" and not pd.isnull(meta[key]):
                    obj = {}
                    metadata.append(obj)
                    obj["label"] = key
                    if key == "帖数":
                        obj["value"] = "『捃拾帖』第" + str(meta[key]) + "帖"
                    else:
                        obj["value"] = meta[key]

                    description += "<tr><th>" + key + "</th>"
                    if key == "帖数":
                        description += "<td><a href='" + df["@id"] + "'>" + "『捃拾帖』第" + str(
                            meta[key]) + "帖" + "</a></td></tr>"
                        # description += "<td><a href='" + relations[df["@id"]] + "'>" + "『捃拾帖』第" + str(
                        #     meta[key]) + "帖" + "</a></td></tr>"
                    else:
                        description += "<td>" + str(meta[key]) + "</td></tr>"

                if key == "帖数":
                    page = "『捃拾帖』第" + str(meta[key]) + "帖"
                if key == "タイトル":
                    title = meta[key]

            df["label"] = title + "（" + page + "のうち）"

            description += "</table>"
            member["description"] = description

            count += 1

        with open("../../docs/data/curation/" + o_name + ".json", 'w') as outfile:
            json.dump(df, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


cflg = True
cpage = 1

data_dir = "data"

list = get_list("../" + data_dir + "/metadata.xlsx")
# relations = {}
import csv

'''
with open(data_dir+'/relations.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        relations[row[0]] = row[1]
'''

while cflg:

    endpoint = "https://diyhistory.org/public/omekac/api"

    curl = endpoint + "/collections?page=" + str(cpage)
    print("curl:\t" + curl)

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

            flg = False

            element_texts = obj["element_texts"]
            for e in element_texts:

                if e["element"]["id"] == 50:
                    org_label = e["text"]
                elif e["element"]["id"] == 48:
                    org_manifest = e["text"]
                    org_canvas = org_manifest.replace("manifest", "canvas")
                elif e["element"]["id"] == 38:
                    vol = int(e["text"])
                    if vol >= 16:
                        flg = True

            if flg:
                exec2collection(org_canvas, org_label, org_manifest)

    else:
        cflg = False
