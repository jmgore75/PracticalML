# Presentation options

Try:
[Reveal.js]()

Backup:
PowerPoint


The presentation should look nice.  Where possible use animations/transitions to move between slides and parts.  

- A demo of Random forest where each tree gets a classification map, and as these maps are combined it forms a more general approximation

- Maps of a variety of classifiers (including nn) versus data points

```py
%matplotlib inline
import time
import pylab as pl
from IPython import display
for i in range(10):
    pl.plot(pl.randn(100))
    display.clear_output(wait=True)
    display.display(pl.gcf())
    time.sleep(1.0)
```

<https://mpld3.github.io/examples/random_walk.html> and <http://mpld3.github.io/notebooks/mpld3_demo.html> shows how to tweak d3 from mpld3.  <http://www.xavierdupre.fr/blog/2013-11-30_nojs.html>

Also consider more modern non-matplotlib implementations like bokeh and vincent