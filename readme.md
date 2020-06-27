# Philosophical Graphiti
> Explore relationships among philosophical topics

Philosophical Graphiti shows you paths between and neighbors of philosophical topics generated from a directed graph formed by the "related" links on [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/index.html) (SEP) articles. It's general enough that it could do the same for other graphs of modest size without much modification.

The site currently works by keeping a single [Networkx](https://networkx.github.io/documentation/stable/index.html) digraph object in memory (basically a dict of dicts). Node attributes (like titles and links to articles) are stored in the database, but edges are not. Because the SEP graph is relatively small, this has worked surprisingly well, even during modest load testing on a "hobby" heroku dyno. The breadth-first nearest neighbors searches tend to be small because of the stucture of this graph (the longest ). I plan to write a post about some more properties of this graph that I explored during development.

The server generates a [Vega](https://vega.github.io/vega/) visualization specification, which, thanks to [Vega-Embed](https://github.com/vega/vega-embed) on the front end, results in an interactive [canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) element in the browser. One of my goals was to allow the user to manipulate the way the graph appears to their liking, while still coming up with a pretty good "default" presentation most of the time. Vega exposes a simulator of physical forces on particles (based on [d3-force](https://github.com/d3/d3-force)), which it calls a "force transform"; this allowed me to get pretty close to what I had in mind; I can also use Django's template system to easily change specifications in the JSON based on the graph structure, user-agent, etc. For instance, I initially present touch users with bigger nodes to make it easier for them to manipulate the graph. The specifications are flexible and deep, and once you get used to the grammar model behind its design, you can express a wide range of user, data, and mark interactions in a relatively small JSON string passed as a variable to the renderer. (I would be perfectly happy to see some more examples throughout the documentation, though!)




![](header.png)

## Usage

### Capture image from a connected video source

Webcam usage requires [ImageSnap](http://iharder.sourceforge.net/current/macosx/imagesnap/) (```$ brew install imagesnap```) and uses the first camera (```$ imagesnap -l```) if multiple are installed. The webcam image will be saved as snapshot.jpg.

### After you clone the project:

1. Run the requirements.txt: ```$ pip install -r requirements.txt```
2. Run asciiart.py: ```$ python asciiart.py -f 'sample.jpg'```

You may need to change your font size to see the whole output, or try changing the width with ```-w [WIDTH]```.

The following options are supported:
* ```-f [filename]```: Path to image file to process; omit to use webcam.
* ```-c```: Render in 256-bit color against black background if your environment supports it
* ```-m```: Method for calculating pixel density. (Default='lightness')
    * ```'mean'```: Average of pixel red, green, and blue values
    * ```'lightness'```: Average of minimum and maximum of red, green, and blue values
    * ```'luminosity'```: Weighted average of red, green, and blue values (0.21R + .72G + .07B) to account for human perception
* ```-w [WIDTH]```: Width of ASCII image before applying width scalar (see below). (Default=80)
* ```-s [SCALE]```: Width scalar of 1, 2, or 3 to compensate for the fact that characters are taller than they are wide. Doubles or triples each character printed to the terminal. (Default=2)

---

Justin Reppert

Script was written on Python 3.7.4

Distributed under the MIT license. See ``LICENSE`` for more information.