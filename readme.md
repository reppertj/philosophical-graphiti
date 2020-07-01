# Philosophical Graphiti
> Explore relationships among philosophical topics

[Philosophical Graphiti](https://www.philosophy.graphics) shows you paths between and neighbors of philosophical topics generated from a directed graph formed by the "related" links on [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/index.html) (SEP) articles. It's general enough that it could do the same for other graphs of modest size without much modification.

The site currently works by keeping a single [Networkx](https://networkx.github.io/documentation/stable/index.html) digraph object (basically a dict of dicts) in memory and only querying the database to return metadata. Node attributes (like titles and links to articles) are stored in the database, but edges are not. Because the SEP graph is relatively small, this has worked surprisingly well, even during modest load testing on a "hobby" heroku dyno.

The server generates a [Vega](https://vega.github.io/vega/) visualization specification, which, thanks to [Vega-Embed](https://github.com/vega/vega-embed) on the front end, results in an interactive [canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) element in the browser. One of my goals was to allow the user to manipulate the way the graph appears to their liking (and save the result), while still coming up with a pretty good "default" presentation most of the time. Vega includes a basic particle simulation (based on [d3-force](https://github.com/d3/d3-force)), which allowed me to get pretty close to what I had in mind; I can also use Django's template system to easily change specifications in the JSON based on the graph structure, user-agent, etc. For instance, I initially present touch users with bigger nodes to make it easier for them to manipulate the graph. The specifications are flexible and deep, and once you get used to the grammar model behind its design, you can express a wide range of user, data, and mark interactions in a relatively small JSON string passed as a variable to the renderer.

![Animation of the Philosophical Graphiti website](header.gif)

---

Justin Reppert

Distributed under the MIT license. See ``LICENSE`` for more information.