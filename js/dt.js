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
  temp.shuffle();
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
  this.leaf = ((depth + 1) >= levels || Math.random() < pBreak);
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

function Graph(rootWidth, levels, classes) {
  this.n = 0;
  this.steps = [];

  rootWidth = rootWidth || 1;
  this.depth = 0;
  this.levels = levels || 4;
  this.classes = classes || 2;
  var level = [];
  for (var i = 0; i < rootWidth; i++) {
    level.push(this.makeNode(i, rootWidth, 0));
  }
  this.depth++;
  this.lastLevel = level;
  this.maxWidth = rootWidth;
  this.steps.push({duration:250, nodes:level, edges:[]});
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

    var source, node, step, i, j;
    step = this.steps[this.steps.length-1];
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = {
        source:source,
        duration:250,
        nodes:step.nodes.slice(0),
        edges:step.edges.slice(0)
      };
      var classes = idArray(this.classes);
      for (j = 0; j < 2; j++) {
        node = this.makeNode(2 * i + j, n, pBreak);
        step.nodes.push(node);
        step.edges.push(this.makeEdge(source, node));
        if (node.leaf) {
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
    step = this.steps[this.steps.length-1];
    for (i = 0; i < this.lastLevel.length; i++) {
      source = this.lastLevel[i];
      step = {
        source:source,
        nodes:step.nodes.slice(0),
        edges:step.edges.slice(0)
      };
      for (j = 0; j < 2; j++) {
        k = temp[2*i + j];
        //TODO handle non-DAG leaf closure?
        while (k >= level.length) {
          node = this.makeNode(k, width);
          step.nodes.push(node);
          level.push(node);
          if (node.leaf) {
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
  randomTree : function (pBreak) {
    while (this.depth < this.levels && this.lastLevel.length) {
      this.treeLevel(pBreak);
    }
  },
  randomDag : function (width) {
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
  }
};

var classPallete = d3.scale.category10();

function nodeDisplay(d) {
  return d.leaf ? classPallete[d.class] : "lightsteelblue";
}

function getId(d) {
  return d.id;
}

var duration = 250;

function displayGraph(svg, graph) {
  var job = {
    interrupt: false,
  };
  var h = svg.attr("height");
  var w = svg.attr("width");
  var s = Math.min(h / graph.levels, w / graph.maxWidth) / 15;

  //Add targets of a node
  function update(step, controller) {
    controller = controller || svg;
    controller = controller.transition()
      .duration(step.duration);

    var node = svg.selectAll("g.node")
      .data(step.nodes, getId);

    var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .attr("transform", function(d) {
        var source = step.source || d;
        return "translate(" + source.x * w + "," + source.y * h + ")";
      });

    nodeEnter.append("svg:circle")
      .attr("r", 1e-6)
      .style("fill", nodeDisplay);

    var nodeUpdate = node.transition()
      .duration(step.duration || 0)
      .attr("transform", function(d) {
        return "translate(" + d.x * w + "," + d.y * h + ")";
      });

    nodeUpdate.select("circle")
      .attr("r", 5 * s);

    node.exit().transition()
      .duration(step.duration || 0)
      .select("circle")
      .style("opacity", 0)
      .remove();

    // Update the links…
    var link = svg.selectAll("path.link")
      .data(step.edges, getId);

/*
    var diagonal = d3.svg.diagonal()
      .projection(function(d) {
        return [d.x * w, d.y * h];
      });
      */
    var diagonal = function (d) {
      var s = [];
      s.push("M");
      s.push(d.source.x * w);
      s.push(d.source.y * h);
      s.push(d.target.x * w);
      s.push(d.target.y * h);
      s.push("z");
      return s.join(" ");
    }

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var source = step.source || d.source;
        return diagonal({
          source: d.source,
          target: source
        });
      });

      // Transition links to their new position.
      link.transition()
        .duration(duration)
        .attr("d", diagonal);

    link.exit().transition()
      .duration(step.duration || 0)
      .style("opacity", 0)
      .remove();

    return controller;
  }

  var controller = svg.transition().duration(0);
  //Update each on a timer
  graph.steps.forEach(function (step) {
    if (job.interrupt) {
      controller
        .interrupt() // cancel the current transition
        .transition();
      controller = update(graph.steps[graph.steps.length + 1]);
    }
    controller.each(function () {
      controller = update(step);
    });
  });

  return job;
}
