import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph, plugin
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import unicodedata

def form(data):
    return unicodedata.normalize("NFKC", data)

json_path = "data/metadata.xlsx.json"

with open(json_path) as f:
    df = json.load(f)

result = []

dcterms = "http://purl.org/dc/terms/"
foaf = "http://xmlns.com/foaf/0.1/"
archiveshub = "http://data.archiveshub.ac.uk/def/"
bibo = "http://purl.org/ontology/bibo/"

# 表示用項目
arr = [dcterms+"description", dcterms+"extent", dcterms+"date", dcterms+"coverage", dcterms+"type", dcterms+"format", dcterms+"subject"]

for i in range(len(df)):
    obj = df[i]

    obj3 = {}
    result.append(obj3)

    obj3["obj"] = obj

    obj2 = []
    obj3["row"] = obj2

    obj2.append("")

    obj2.append('<a onclick="show_curation_modal(\''+obj[dcterms+"relation"][0]["@id"]+'\'); return false;"><span style="display : none;">true</span><img class="lazy z-depth-1" style="max-height:151px; max-width:200px;" data-src="'+obj[foaf+"thumbnail"][0]["@id"]+'"></a>')
    obj2.append(form(obj[dcterms+"title"][0]["@value"]))
    obj2.append("『捃拾帖』第"+str(obj[bibo+"volume"][0]["@value"])+"帖")
    obj2.append('<span style="display : none;">'+str(obj[archiveshub+"note"][0]["@value"])+'</span>'+obj[dcterms+"identifier"][0]["@value"])
    for e in arr:
        text = ""
        if e == dcterms+"date":
            text = "<span style='display : none;'>"+str(obj[archiveshub+"dateCreatedAccumulated"][0]["@value"])+"</span>"+obj[archiveshub+"dateCreatedAccumulatedString"][0]["@value"]
        elif e in obj:
            tmp = obj[e]
            for j in range(len(tmp)):
                text += tmp[j]["@value"]

                if j != len(tmp) - 1:
                    text += "・"

            # text = obj[e][0]["@value"]

        obj2.append(form(text))

    obj2.append('<a href="iiif-curation-player/?curation='+obj[dcterms+"relation"][0]["@id"]+'" target="cr"><img src="assets/images/icp-logo.png"></a>')

with open("data/table.json", 'w') as f:
    json.dump(result, f, ensure_ascii=False, sort_keys=True, separators=(',', ': '))