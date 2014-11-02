tag-graph-map-of-stackexchange
==============================

**[Click here too see graph visualizations of StackExchange](https://github.com/stared/tag-graph-map-of-stackexchange/wiki)**.

See also: **[TagOverflow](http://stared.github.io/tagoverflow/)**.

# Development

I wrote scripts generating a map of topics from [StackExchange sites](http://stackexchange.com/sites) (e.g. [StackOverflow](http://stackoverflow.com)),
in form of a graph of tags. Started as [an entry for StackExchange visualization competition at Kaggle](https://www.kaggle.com/c/predict-closed-questions-on-stack-overflow/prospector#211).

If you like pictures, visit [wiki for this GitHub project](https://github.com/stared/tag-graph-map-of-stackexchange/wiki).
However,  if you want to read the documentation - read below.

To do:

* interactive d3js graphs
* plots for Area51
* automated plots

Current state:

* with queries from [SE Data Explorer](http://data.stackexchange.com) (but it works for any other csv tables for any other tags, as long as it is in the same form)
* with API scrapers to get tags from beta sites and to make a map of the StackExchange network
* **further development moved to [TagOverflow](http://stared.github.io/tagoverflow/)** - an interactive tag visualization in d3.js

==============================

# Usage

## Mature SE sites

data.stackexchange.com -> csv -> oetable2graphml.py -> graphml -> gephi -> pdf


- To get data, use [a data.SE query](http://data.stackexchange.com/stackoverflow/query/83415/)
to obtain table of tag [co-occurrences](http://stats.stackexchange.com/questions/40977/is-there-a-term-for-pa-cap-b-papb);
[my other queries](http://data.stackexchange.com/users/8877/piotr-migdal)

- Run oetable2graphml.py to convert it to graphml file (requires [NetworkX](http://networkx.lanl.gov/)), e.g.

<code>python oetable2graphml.py input.csv output.graphml</code>

- Use [Gephi](http://gephi.org) to import graphml file and process it to your taste.<br>
E.g. (on Gephi 0.8.1 beta): 

* Overview tab:
 * Ranking -> Nodes -> Size -> weight -> Min:15, Max:30, Spline:3 -> Run <br>
  (optimal options may vary)
 * Layout -> ARF -> Run <br>
  OR: Layout -> Force Atlas -> Run; Layout -> Fruchterman Reingold -> Run <br>
  (and you may like to experiment with parameters or other methods)
 * Layout -> Noverlap -> Run
 * Statistics -> Modularity -> Run
 * Partition -> Nodes -> Refresh -> Modularity Class -> Apply <br>
  (and optionally choosing colors to your taste)
 * Font size: 26pt, Node size, Show node labels
 * Layout -> Label Adjust -> Run
* Preview tab: 
 * Nodes -> Border Color: #A0A0A0
 * Node Labels -> Show Labels: True, Font: 4pt  
 * Edges -> Opacity: 40.0
 * Refresh; Export


## Beta sites and other tags

First, obtain tag bundles with SE API, e.g. [se-api-py](https://github.com/stared/se-api-py), e.g. doing:

	x = se.fetch("questions", site="biology", filter="!nR5-WLw0-5")  # filter says that we ask only for the 'tags' field
	t = [y['tags'] for y in x]

You need to have list of list with tags per post, e.g.

	t = [["plants", "flowers"], ["plants", "carnivorous", "big-list"], ["carnivorous", "fish", "piranha"]]

Then process it e.g. in that way:

	import tag_bundle_processing as tbp
	bun = tbp.Bundle(t) 
	# or: bun = tbp.Bundle(json_path="data.json")

	bun.filter_elements(first_n=32)  # takes only 32 most frequent tags
	bun.calculate_pair_weights(self, func=oe_ratio, threshold=1.5)
	bun.export2graphml("path/to/file.graphml")

And then proceed use Gephi as for mature SE sites.
