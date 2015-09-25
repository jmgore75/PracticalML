//shuffle an array
Array.prototype.shuffle = function () {
  if (this.length) {
    for(var j, x, i = this.length; i; j = Math.floor(Math.random() * i), x = this[--i], this[i] = this[j], this[j] = x);
  }
  return this;
};

//pop a random item in an array
Array.prototype.rpop = function () {
  if (!this.length) {
    throw "Cannot rpop from empty array";
  }
  return this.splice(Math.floor(Math.random() * this.length), 1)[0];
};

function idArray(count) {
  var a = [];
  for (i = 0; i < count; i++) {
    a.push(i);
  }
  return a;
}

function Edge(source, target) {
  this.source = source;
  this.target = target;
  source.edges.push(this);
  target.edges.push(this);
}

function Node(pos, peers, depth, levels, pBreak) {
  pBreak = pBreak || 0;
  this.depth = depth;
  this.pos = pos;
  this.edges = [];
  this.x = (2 * pos + 1) / (2 * peers);
  this.y = (2 * depth + 1) / (2 * levels);
  this.label = ((depth + 1) >= levels || Math.random() < pBreak);
}
Node.prototype = {
  sources : function () {
    var self = this;
    return this.edges.filter(function (edge) {
      return edge.target === self;
    });
  },
  targets : function () {
    var self = this;
    return this.edges.filter(function (edge) {
      return edge.source === self;
    });
  }
};

function Step(graph, duration, source) {
  this.graph = graph;
  this.duration = duration || 0;
  this.source = source || undefined;
  this.nodes = [];
  this.edges = [];
}
Step.prototype = {
  initialize : function (prior) {
    this.nodes = prior && prior.nodes ? prior.nodes.slice(0) : [];
    this.edges = prior && prior.edges ? prior.edges.slice(0) : [];
  },
  addNodes : function (nodes) {
    if (nodes && nodes.length) {
      this.nodes = this.nodes.concat(nodes);
    }
  },
  addEdges : function (edges) {
    if (edges && edges.length) {
      this.edges = this.edges.concat(edges);
    }
  }
};

function Graph(levels, classes) {
  this.nextId = 0;
  this.steps = [];
  this.depth = 0;
  this.maxWidth = 0;
  this.levels = levels || 4;
  this.classes = classes || 2;
}
Graph.prototype = {
  lastStep : function () {
    if (this.steps.length) {
      return this.steps[this.steps.length-1];
    }
  },
  newStep : function (duration, source) {
    var step = new Step(this, duration, source);
    var prior = this.lastStep();
    if (prior) {
      step.initialize(prior);
    }
    return step;
  },
  makeNode : function(pos, peers, pBreak) {
    var node = new Node(pos, peers, this.depth, this.levels, pBreak);
    node.id = this.nextId++;
    return node;
  },
  makeEdge : function (source, target) {
    var edge = new Edge(source, target);
    edge.id = this.nextId++;
    return edge;
  },
  finish : function () {
    this.lastLevel = [];
    this.complete = this.newStep(0);
  },
  splitDuration : 200,
  layerDuration : 500,
  startLevel : function (width, isFeature) {
    width = width || 1;
    var level = [];
    for (var i = 0; i < width; i++) {
      var node = this.makeNode(i, width, 0);
      node.feature = isFeature ? true : false;
      level.push(node);
    }
    var root = this.newStep(this.layerDuration);
    root.addNodes(level);
    this.steps.push(root);
    this.depth++;
    if (width > this.maxWidth) {
      this.maxWidth = width;
    }
    this.lastLevel = level;
  },
  treeLevel : function(pBreak) {
    if (!this.lastLevel.length) {
      throw "No prior levels";
    }

    pBreak = pBreak || 0;
    var level = [];
    var n = this.lastLevel.length * 2;

    var source, node, step, i, j;
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = this.newStep(this.splitDuration, source);
      var classes = idArray(this.classes);
      for (j = 0; j < 2; j++) {
        node = this.makeNode(2 * i + j, n, pBreak);
        step.nodes.push(node);
        step.edges.push(this.makeEdge(source, node));
        if (node.label) {
          node.class = classes.rpop();
        } else {
          level.push(node);
        }
      }
      this.steps.push(step);
    }
    this.depth++;
    if (n > this.maxWidth) {
      this.maxWidth = n;
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

    var source, node, step, i, j;
    var temp = [];
    for (i = 0; i < width; i++) {
      temp.push(i);
    }
    while (temp.length < this.lastLevel.length * 2) {
      temp.push(Math.floor(width * Math.random()));
    }
    temp.shuffle();
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
    var classes = idArray(this.classes);
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = this.newStep(this.splitDuration, source);
      for (j = 0; j < 2; j++) {
        k = temp[2*i + j];
        //TODO handle non-DAG label closure?
        while (k >= level.length) {
          node = this.makeNode(k, width);
          step.nodes.push(node);
          level.push(node);
          if (node.label) {
            node.class = classes.rpop();
          } else {
            nextPrior.push(node);
          }
        }
        node = level[k];
        step.edges.push(this.makeEdge(source, node));
      }
      this.steps.push(step);
    }
    this.depth++;
    if (width > this.maxWidth) {
      this.maxWidth = width;
    }
    this.lastLevel = nextPrior;
  },
  fullLevel: function (width) {
    if (width < 1) {
      throw "Level is too narrow";
    }
    if (!this.lastLevel.length) {
      throw "No prior levels";
    }

    var level = [];
    var nextPrior = [];
    var source, step, node, i, j;
    step = this.newStep(this.layerDuration);
    for (i = 0; i < width; i++) {
      node = this.makeNode(i, width);
      step.nodes.push(node);
      level.push(node);
      if (node.label) {
        node.class = i;
      } else {
        nextPrior.push(node);
      }
    }
    this.steps.push(step);

    step = this.newStep(this.layerDuration);
    for (i = 0; i < width; i++) {
      node = level[i];
      for (j = 0; j < this.lastLevel.length; j++) {
        source = this.lastLevel[j];
        step.edges.push(this.makeEdge(source, node));
      }
    }
    this.steps.push(step);

    this.depth++;
    if (width > this.maxWidth) {
      this.maxWidth = width;
    }
    this.lastLevel = nextPrior;
  }
};
Graph.prototype.type = "path";

function Tree(depth, classes, pBreak) {
  Graph.call(this, depth, classes);
  this.startLevel(1);
  while (this.depth < this.levels && this.lastLevel.length) {
    this.treeLevel(pBreak);
  }
  this.finish();
}
Tree.prototype = Object.create(Graph.prototype);

function DAG(depth, classes, width) {
  Graph.call(this, depth, classes);
  this.startLevel(1);
  width = width || 10;
  while (this.depth < this.levels) {
    if (this.depth + 1 === this.levels) {
      this.dagLevel(this.classes);
    } else if (this.lastLevel.length * 2 > width) {
      this.dagLevel(width);
    } else {
      this.treeLevel();
    }
  }
  this.finish();
}
DAG.prototype = Object.create(Graph.prototype);

function NN() {
  var hidden = Array.prototype.slice.call(arguments);
  var depth = hidden.length;
  var features = hidden.shift();
  var classes = hidden.pop();
  Graph.call(this, depth, classes);
  this.startLevel(features, true);
  for (i = 0; i < hidden.length; i++) {
    this.fullLevel(hidden[i]);
  }
  this.fullLevel(classes);
  this.finish();
}
NN.prototype = Object.create(Graph.prototype);
NN.prototype.type = "linear";

var classPallete = d3.scale.category10();

function nodeDisplay(d) {
  return d.label ? classPallete(d.class || 0) : "lightsteelblue";
}

function getId(d) {
  return d.id;
}

var clearStep = new Step({
  levels:1,
  maxWidth:1
}, 400);

function displayStep(step, svg, duration) {
  if (duration === undefined) {
    duration = step.duration;
  }
  duration = duration || 0;

  var dotr = 5;
  var sw = step.graph.type === "path" ? 2 : 0.25;

  var h = svg.attr("height");
  var w = svg.attr("width");
  var s = Math.min(h / step.graph.levels, w / step.graph.maxWidth) / (3 * dotr);

  var diagonal = function (d) {
    var s = [];
    s.push("M");
    s.push(d.source.x * w);
    s.push(d.source.y * h);
    s.push(d.target.x * w);
    s.push(d.target.y * h);
    s.push("z");
    return s.join(" ");
  };

  var node = svg.selectAll("g.node")
    .data(step.nodes, getId);

  // Update the links…
  var link = svg.selectAll("path.link")
    .data(step.edges, getId);

  var nodeEnter = node.enter().append("svg:g")
    .attr("class", "node")
    .attr("transform", function(d) {
      var source = step.source || d;
      return "translate(" + source.x * w + "," + source.y * h + ")";
    });

  nodeEnter.each(function (d) {
    var e = d3.select(this);
    if (d.label || d.feature) {
      e.append("svg:rect")
        .attr("width", 0)
        .attr("height", 0)
        .attr("x", 0)
        .attr("y", 0)
        .style("fill", nodeDisplay);
    } else {
      e.append("svg:circle")
        .attr("r", 0)
        .style("fill", nodeDisplay);
    }
  });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
    .attr("class", "link")
    .style("stroke-width", 0)
    .attr("d", function(d) {
      var source = step.source || d.source;
      return diagonal({
        source: d.source,
        target: source
      });
    });


  var nodeUpdate = node;
  var nodeExit = node.exit();
  var linkUpdate = link;
  var linkExit = link.exit();

  if (duration) {
    nodeUpdate = nodeUpdate.transition()
      .duration(duration);
    nodeExit = nodeExit.transition()
        .duration(duration);
    linkUpdate = linkUpdate.transition()
          .duration(duration);
    linkExit = linkExit.transition()
          .duration(duration);
  }

  nodeUpdate.attr("transform", function(d) {
      return "translate(" + d.x * w + "," + d.y * h + ")";
    });

  nodeUpdate.select("circle")
    .attr("r", dotr * s);

  nodeUpdate.select("rect")
    .attr("width", 2 * dotr * s)
    .attr("height", 2 * dotr * s)
    .attr("x", -dotr * s)
    .attr("y", -dotr * s);


  nodeExit.select("circle")
    .attr("r", 0);

  nodeExit.select("rect")
    .attr("width", 0)
    .attr("height", 0)
    .attr("x", 0)
    .attr("y", 0);

  nodeExit
    .remove();


  // Transition links to their new position.
  linkUpdate
    .style("stroke-width", sw)
    .attr("d", diagonal);

  linkExit.style("opacity", 0)
    .style("stroke-width", 0)
    .remove();

}
