var diagonal = d3.svg.diagonal()
  .projection(function(d) {
    return [d.y, d.x];
  });

//shuffle an array
function shuffle(o){
  for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
  return o;
}

function pickOneOrMoreInOrder(options, pick) {
  if (pick < options) {
    throw "Must have more picks than options";
  }
  var temp = [];
  for (i = 0; i < options; i++) {
    temp.push(i);
  }
  while (temp.length < pick) {
    temp.push(Math.floor(options * Math.random()));
  }
  shuffle(temp);
  var map = [];
  return temp.map(function (i) {
    var j = map.indexOf(i);
    if (j < 0) {
      j = map.length;
      map.push(i);
    }
    return j;
  });
}

function Edge(source, target) {
  source.targets.push(target);
  target.sources.push(source);
  this.source = source;
  this.target = target;
}

function Node(pos, peers, depth, levels, pBreak) {
  pBreak = pBreak || 0;
  var node = {};
  this.depth = depth;
  this.pos = pos;
  this.sources = [];
  this.targets = [];
  this.xpos = (2 * pos + 1) / (2 * peers);
  this.ypos = (2 * depth + 1) / (2 * levels);
  this.leaf = ((depth + 1) >= levels || Math.random() < pBreak);
  return node;
}

function Graph(levels, classes) {
  this.n = 0;
  this.classes = classes;
  this.levels = levels || 4;
  this.root = this.makeNode(0, 1, 0);
  this.lastLevel = [this.root];
  this.depth = 1;
  this.steps = [{source:this.root, nodes:this.lastLevel, edges:[]}];
}
Graph.prototype = {
  makeNode : function(pos, peers, pBreak) {
    var node = new Node(pos, peers, this.depth, this.levels, pBreak);
    node.id = this.n++;
    return node;
  },
  makeEdge : function (source, target) {
    var edge = new Edge(source, target);
    edge.id = this.n++;
    return edge;
  },
  treeLevel : function(pBreak) {
    if (!this.lastLevel.length) {
      throw "No prior levels";
    }

    pBreak = pBreak || 0;
    var level = [];
    var n = this.lastLevel.length * 2;

    this.depth++;
    var source, node, step, i, j;
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = {source:source, nodes:[], edges:[]};
      //TODO setup classes
      for (j = 0; j < 2; j++) {
        node = this.makeNode(2 * i + j, n, pBreak);
        step.nodes.push(node);
        step.edges.push(this.makeEdge(source, node));
        if (node.leaf) {
          //node clases
        } else {
          level.push(node);
        }
      }
      this.steps.push(step);
    }
    this.lastLevel = level;
  },
  dagLevel: function(width) {
    if (width < 2) {
      throw "Level is too narrow";
    }
    if (!this.lastLevel.length) {
      throw "No prior levels";
    }
    if (width > this.lastLevel.length * 2) {
      throw "Level is too wide";
    }


    this.depth++;
    var source, node, step, i, j;
    var temp = [];
    for (i = 0; i < width; i++) {
      temp.push(i);
    }
    while (temp.length < this.lastLevel.length * 2) {
      temp.push(Math.floor(width * Math.random()));
    }
    shuffle(temp);
    var level = [];
    for (i = 0; i < temp.length; i++) {
      j = level.indexOf(temp[i]);
      if (j < 0) {
        j = level.length;
        level.push(temp[i]);
      }
      temp[i] = j;
    }

    level = [];
    var nextPrior = [];
    var k;
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = {source:source, nodes:[], edges:[]};
      for (j = 0; j < 2; j++) {
        k = temp[2*i + j];
        while (k >= level.length) {
          node = this.makeNode(k, n);
          step.nodes.push(node);
          level.push(node);
          if (!node.leaf) {
            nextPrior.push(node);
          }
        }
        node = level[k];
        step.edges.push(this.makeEdge(source, node));
      }
      this.steps.push(step);
    }
    this.lastLevel = nextPrior;
  },
  randomTree : function (pBreak) {
    while (this.depth < this.levels) {
      this.treeLevel(pBreak);
    }
  },
  randomDag : function (width) {
    width = width || 10;
    classes = classes || width;
    while (this.depth < this.levels) {
      if (this.depth + 1 === this.levels) {
        this.dagLevel(this.classes);
      } else if (this.lastLevel.length * 2 > width) {
        this.dagLevel(width);
      } else {
        this.treeLevel();
      }
    }
  }
};

function nodeDisplay(d) {
  return d.leaf ? "red" : "blue";
}

function getId(d) {
  return d.id;
}

var duration = 250;

function displayGraph(svg, graph, duration) {
  var job = {
    interrupt: false,
  };

  //Add targets of a node
  function update(step) {
    var existingNode = svg.selectAll("g.node");

    var node = existingNode
      .data(step.nodes, getId);

    var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .attr("transform", function(d) {
        return "translate(" + step.source.y + "," + step.source.x + ")";
      });

    nodeEnter.append("svg:circle")
      .attr("r", 1e-6)
      .style("fill", nodeDisplay);

    var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function(d) {
        return "translate(" + d.y + "," + d.x + ")";
      });

    nodeUpdate.select("circle")
      .attr("r", 4.5);

    // Update the links…
    var link = svg.selectAll("path.link")
      .data(step.edges, getId);

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        return diagonal({
          source: node.data().d.source,
          target: d.source
        });
      });

    // Transition links to their new position.
    link.transition()
      .duration(duration)
      .attr("d", diagonal);

    return nodeUpdate;
  }

  var transition;
  //Update each on a timer
  graph.steps.forEach(function (step) {
    if (job.interrupt) {
      selection
        .interrupt() // cancel the current transition
        .transition();
    }
    var source = d3.select(step.source);
    source.transition.
    function
    transition = transition ? transition.each("end", function () {
      update(node);
    }) : update(node)
    setInterval(function() {
      update(node);
    }, duration);
  });

  return job;
}
