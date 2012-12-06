import csv
import sys
import networkx as nx


def oecsv2graphml(input_path, output_path="output.graphml",
                  threshold=0.):
    with open(input_path, "r") as f:
        data = list(csv.reader(f))[1:]
    data = map(lambda x: [x[0], x[1], float(x[2]), int(x[3]), int(x[4]), int(x[5])], data)
    nodes = dict([(x[0], x[3]) for x in data]
                 + [(x[1], x[4]) for x in data])

    G = nx.Graph()
    for k, v in nodes.items():
        G.add_node(k, weight=v)

    data_filtered = filter(lambda x: x[2] >= threshold, data)
    for x in data_filtered:
        G.add_edge(x[0], x[1], weight=x[2])

    nx.write_graphml(G, output_path)
    print "Saved!\nNodes: %d\tEdges: %d out of %d" % (len(nodes), len(data_filtered), len(data))


if __name__ == "__main__":
    oecsv2graphml(*sys.argv[1:])
