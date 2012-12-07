from collections import defaultdict
import networkx as nx
try:
    import simplejson as json
except:
    import json


def oe_ratio(n, nx, ny, nxy):
    return float(n) * float(nxy) / (float(nx) * float(ny))

def cooccurrences(n, nx, ny, nxy):
    return float(nxy)


class Bundle():
    def __init__(self, li=[], json_path=""):
        if json_path:
            with open(json_path, "r") as f:
                li = json.load(f)
        self.total = len(li)
        self.elements_dict_full = self.bundles2tags(li)
        self.pairs_dict_full = self.bundles2pairs(li)
        self.filter_elements()

    def filter_elements(self, min_counts=0, first_n=0):
        self.elements = self.elements_dict_full.items()
        self.elements.sort(key=lambda x: -x[1])

        if first_n:
            self.elements = self.elements[:first_n]
        if min_counts:  # if not necessary, but can make it faster
            self.elements = filter(lambda x: x[1] >= min_counts, self.elements)

        elements_dict = dict(self.elements)  # just to make "in" quicker

        self.pairs = self.pairs_dict_full.items()
        self.pairs = filter(lambda x: x[0][0] in elements_dict
                            and x[0][1] in elements_dict,
                            self.pairs)
        self.pairs.sort(key=lambda x: -x[1])
        return {"elements": len(self.elements), "pairs": len(self.pairs)}

    def calculate_pair_weights(self, func=oe_ratio, threshold=0.):
        elements_dict = dict(self.elements)
        self.pairs_weighted = [(xy, func(n=self.total, nx=elements_dict[xy[0]],
                                ny=elements_dict[xy[1]], nxy=nxy))
                               for xy, nxy in self.pairs]
        self.pairs_weighted = filter(lambda x: x[1] >= threshold,
                                     self.pairs_weighted)
        self.pairs_weighted.sort(key=lambda x: -x[1])
        return len(self.pairs_weighted)

    def bundles2tags(self, li):
        """For a list with elements being lists, counts all elements inside,
           e.g. [[1, 6, 2], [3], [3, 1, 2]] -> defaultdict{1:2, 2:2, 3:2, 6:1}"""
        res = defaultdict(lambda: 0)
        for bundle in li:
            for x in bundle:
                res[x] += 1
        return res

    def bundles2pairs(self, li):
        """For a list with elements being lists, counts all lexically ordered pairs,
           e.g. [[1, 6, 2], [3], [3, 1, 2]] -> defaultdict{(1,2):2, (1,3):1, (1,6):1}"""
        res = defaultdict(lambda: 0)
        for bundle in li:
            for x in bundle:
                for y in bundle:
                    if x < y:
                        res[(x, y)] += 1
        return res

    def export2graphml(self, output_path):  # to do
        G = nx.Graph()
        for k, v in self.elements:
            G.add_node(k, weight=v)

        for x in self.pairs_weighted:
            G.add_edge(x[0][0], x[0][1], weight=x[1])

        nx.write_graphml(G, output_path)
        print "Saved!\nNodes: %d\tEdges: %d" % (len(self.elements), len(self.pairs_weighted))
