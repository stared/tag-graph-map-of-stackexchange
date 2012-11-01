tag-graph-map-of-stackexchange
==============================

Generates map in form of a graph from tags on StackExchange sites, e.g. StackOverflow.

Started as an entry for StackExchange visualization competition at Kaggle:

https://www.kaggle.com/c/predict-closed-questions-on-stack-overflow/prospector#211

Current state:

* with queries from data.stackexchange.com (but it works for any other csv tables
		for any other tags, as long as it is in the same form)
* someother stuff

To do:
* interactive d3js graphs
* plots for beta sites and for Area51 

==============================

And example use:

data.stackexchange.com -> csv -> oetable2graphml.py -> graphml -> gephi -> pdf


- To get data, use a data.SE query to obtain table of tag co-occurrences:

 http://data.stackexchange.com/stackoverflow/query/83415/
	
 more info on the quantity... on StackExchange:

 http://stats.stackexchange.com/questions/40977/is-there-a-term-for-pa-cap-b-papb

 my other queries: http://data.stackexchange.com/users/8877/piotr-migdal

- Run oetable2graphml.py to convert it to graphml file, e.g.

 python oetable2graphml.py input.csv output.graphml

- Use Gephi (http://gephi.org) to import graphml file and process it to your taste.
E.g. (on Gephi 0.8.1 beta): 

* Overview tab:
 * Ranking -> Nodes -> Size -> weight -> Min:15, Max:30, Spline:3 -> Run
  (optimal options may vary)
 * Layout -> ARF -> Run
  OR: Layout -> Force Atlas -> Run; Layout -> Fruchterman Reingold -> Run
   (and you may like to experiment with parameters or other methods)
 * Layout -> Noverlap -> Run
 * Statistics -> Modularity -> Run
 * Partition -> Nodes -> Refresh -> Modularity Class -> Apply
    	(and optionally choosing colors to your taste)
 * Font size: 26pt, Node size, Show node labels
 * Layout -> Label Adjust -> Run
* Preview tab: 
 * Nodes -> Border Color: #A0A0A0
 * Node Labels -> Show Labels: True, Font: 4pt  
 * Edges -> Opacity: 40.0
 * Refresh; Export

