import json
import sys

try:
    data = open("allow.csv", "r").read()
except IOError:
    sys.exit(0)
else:
    data = data.split('\n')
    data = data[1:-1]

labels = set()
classes = ["domain",]
links = []
nodes = []
seen = set()


def find_node(n):
    for i, node in enumerate(nodes):
        if node.get("name") == n:
            return i
    print "Error"


for line in data:
    d, t, c = line.split(", ")
    print d, t, c,
    if c not in labels:
        labels.add(c)
        classes.append(c)
    if d not in labels:
        labels.add(d)
        nodes.append({"name":d, "setype":"domain", "group":classes.index("domain")})
    if t not in labels:
        labels.add(t)
        nodes.append({"name":t, "setype":c, "group":classes.index(c)})
    links.append({"source":find_node(d), "target":find_node(t)})
    print links[-1]


print len(labels),'vs',len(nodes)
print len(links)

with open("../viz/data/allow-dict.json", "w") as fout:
    rv = {"nodes":nodes, "links":links}
    json.dump(rv, fout, indent=4)
