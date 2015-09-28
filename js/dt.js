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

var nextId = 0;

function idArray(count) {
  var a = [];
  for (i = 0; i < count; i++) {
    a.push(i);
  }
  return a;
}

function Edge(source, target) {
  this.id = nextId++;
  this.source = source;
  this.target = target;
  source.edges.push(this);
  target.edges.push(this);
}

function Node(pos, peers, depth, levels, pBreak) {
  pBreak = pBreak || 0;
  this.id = nextId++;
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
    return node;
  },
  makeEdge : function (source, target) {
    var edge = new Edge(source, target);
    return edge;
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
  treeLevel : function(pBreak, condense) {
    if (!this.lastLevel.length) {
      throw "No prior levels";
    }

    pBreak = pBreak || 0;
    var level = [];
    var n = condense ? this.lastLevel.length * 2 : Math.pow(2, this.depth);

    var source, node, step, i, j;
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = this.newStep(this.splitDuration, source);
      var classes = idArray(this.classes);
      for (j = 0; j < 2; j++) {
        node = this.makeNode((condense ? i : source.pos) * 2 + j, n, pBreak);
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

function Tree(depth, classes, pBreak, noCondense) {
  Graph.call(this, depth, classes);
  this.startLevel(1);
  while (this.depth < this.levels && this.lastLevel.length) {
    this.treeLevel(pBreak, !noCondense);
  }
  this.makeLevelSteps();
}
Tree.prototype = Object.create(Graph.prototype);
Tree.prototype.makeLevelSteps = function () {
  var root = this.steps[0];
  var tree = this;
  tree.steps = [root];
  function crawl(node) {
    var targets = node.targets();
    if (targets.length) {
      var step = tree.newStep(tree.splitDuration, node);
      tree.steps.push(step);
      targets.forEach(function (edge) {
        step.edges.push(edge);
        step.nodes.push(edge.target);
      });
      targets.forEach(function (edge) {
        crawl(edge.target);
      });
    }
  }
  root.nodes.forEach(function (node) {
    crawl(node);
  });
};

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
      this.treeLevel(0, true);
    }
  }
}
DAG.prototype = Object.create(Graph.prototype);

function Forest(depth, classes, pBreak, scale, noCondense) {
  scale = scale || 2;
  Graph.call(this, depth * scale, classes);
  var trees = [];
  var maxSteps = 0;
  var maxWidth = 0;
  var i, j, k, tree, step, otherTree, otherStep;
  function posAdjust(node) {
    node.x = (i + node.x) / scale;
    node.y = (j + node.y) / scale;
  }
  for (i = 0; i < scale; i++) {
    for (j = 0; j < scale; j++) {
      tree = new Tree(depth, classes, pBreak, noCondense);
      if (tree.steps.length > maxSteps) {
        maxSteps = tree.steps.length;
      }
      if (tree.maxWidth > maxWidth) {
        maxWidth = tree.maxWidth;
      }
      tree.lastStep().nodes.forEach(posAdjust);
      trees.push(tree);
    }
  }
  var steps = [];
  for (i = 0; i < maxSteps; i++) {
    for (j = 0; j < trees.length; j++) {
      tree = trees[j];
      if (i < tree.steps.length) {
        step = this.newStep(this.splitDuration / 2);
        for (k = 0; k < trees.length; k++) {
          otherTree = trees[k];
          if (k <= j) {
            if (i < otherTree.steps.length) {
              otherStep = otherTree.steps[i];
            } else {
              otherStep = otherTree.lastStep();
            }
          } else if (k > j && i) {
            if ((i-1) < otherTree.steps.length) {
              otherStep = otherTree.steps[i-1];
            } else {
              otherStep = otherTree.lastStep();
            }
          }
          if (k === j) {
            step.source = otherStep.source;
          }
          step.nodes = step.nodes.concat(otherStep.nodes);
          step.edges = step.edges.concat(otherStep.edges);
        }
        steps.push(step);
      }
    }
  }
  this.steps = steps;
  this.maxWidth = maxWidth * scale;
  this.depth = depth * scale;
  this.level = depth * scale;
}
Forest.prototype = Object.create(Graph.prototype);

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

var normal = d3.random.normal();

function norm2d() {
  var m = normal();
  var t = Math.random() * Math.PI;
  var x = m * Math.sin(t);
  var y = m * Math.cos(t);
  return {x:x, y:y};
}

function Target(g, w) {
  this.g = g;
  this.w = w || 5;
  this.r = this.w / 2;
}
Target.prototype = {
  doShots : function (shots, duration) {
    duration = duration || 0;
    duration /= shots.length;
    var pts = this.g.selectAll("circle.shot")
      .data(shots, getId);

    var pte = pts.enter()
      .append("svg:circle")
      .attr("class", "shot")
      .attr("r", this.r)
      .attr("cx", function (d) {return d.x;})
      .attr("cy", function (d) {return d.y;});

    var pto = pts.exit();

    if (duration) {
      pte.style("opacity", 0);

      pts.transition()
        .delay(function (d, i) {
          return (i + (Math.random() - 0.5) / 10)*duration;
        })
        .duration(0)
        .style("opacity", 1);

      pto = pto.transition().duration(500)
        .style("opacity", 0);
    }

    pto.remove();
  }
};

function Shooter(r, t, s) {
  this.r = r;
  this.t = t;
  this.s = s;
  this.x = Math.sin(t) * this.r;
  this.y = Math.cos(t) * this.r;
  this.shots = {};
  this.shots["first-shots"] = this.makeShots(20);
  this.shots["many-shots"] = this.makeShots(100);
}
Shooter.prototype = {
  makeShots : function (n) {
    n = n || 15;
    var data = [];
    for (var i = 0; i < n; i++) {
      var pt = norm2d();
      pt.x = pt.x * this.s + this.x;
      pt.y = pt.y * this.s + this.y;
      pt.id = nextId++;
      data.push(pt);
    }
    return data;
  }
};
