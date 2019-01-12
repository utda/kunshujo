import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import csv
import numpy as np

df = pd.read_excel('data/metadata.xlsx', sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

locations = []

for j in range(3, r_count):
    value = df.iloc[j, 8]
    if value not in locations:
        locations.append(value)

    value = df.iloc[j, 10]
    if value not in locations:
        locations.append(value)

targets = {}

g = Graph()

with open('data/地名.txt', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:

        if row[2] != "2":
            continue

        subject = "http://ja.dbpedia.org/resource/"+row[1]

        if subject not in targets:
            tmp = []
            targets[subject] = tmp
            tmp.append(float(row[4]))
            tmp.append(float(row[5]))


for location in locations:

    if str(location) == "nan":
        continue

    if location not in targets:
        print("*"+location)

    label = location.split("/")[-1]

    subject = URIRef(location)

    g.add((subject, RDFS.label, Literal(label)))

    if label == "大阪":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(34.662762)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(135.572854)))
    elif label == "名古屋":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.170915)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(136.881537)))

    elif label == "中国":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.86166)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(104.195397)))

    elif label == "江戸":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.676666)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(139.762222)))

    elif label == "北海道":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(43.063888)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(141.347777)))

    elif label == "横浜":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.443708)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(139.638026)))

    elif label == "相模国":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.456795)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(139.334884)))

    elif label == "東京":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.709026)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(139.731993)))

    elif label == "京都":
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(35.011636)))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(135.768029)))

    else:
        tmp = targets[location]
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat"), Literal(tmp[0])))
        g.add((subject, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long"), Literal(tmp[1])))


g.serialize(destination='data/map.json', format='json-ld')
