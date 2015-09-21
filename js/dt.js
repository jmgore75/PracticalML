var diagonal = d3.svg.diagonal()
  .projection(function(d) {
    return [d.y, d.x];
  });

function makeNode(pos, peers, depth, levels, pBreak) {
  pBreak = pBreak || 0;
  var node = {};
  node.depth = depth;
  node.pos = pos;
  node.parents = [];
  node.children = [];
  node.xpos = (2 * pos + 1) / (2 * peers);
  node.ypos = (2 * depth + 1) / (2 * levels);
  node.leaf = ((depth + 1) >= levels || Math.random() < pBreak);
  return node;
}

function makeEdge(parent, child) {
  parent.children.push(child);
  child.parents.push(parent);
}

function randomTree(depth, pBreak) {
  depth = depth || 4;
  pBreak = pBreak || 0;

  var id = 0;
  var nodes = [];
  var root = makeNode(0, 1, 0, depth);
  nodes.push(root);

  function treeNode(node, peers) {
    node.id = id++;
    nodes.push(node);
    if (!node.leaf) {
      var child = makeNode(2 * node.pos, peers * 2, node.depth + 1, depth, pBreak);
      makeEdge(node, child);
      treeNode(child);
      child = makeNode(2 * node.pos + 1, peers * 2, node.depth + 1, depth, pBreak);
      makeEdge(node, child);
      treeNode(child);
    }
  }
  treeNode(root, 1);

  return nodes;
}

function randomDag(depth, width, classes) {
  depth = depth || 4;
  width = width || 10;
  classes = classes || width;
  if (classes > width) {
    throw "Number of classes is greater than DAG width";
  }

  var id = 0;
  var nodes = [];
  var root = makeNode(0, 1, 0, depth);
  root.id = id++;
  nodes.push(root);

  var prior = [root];

  var node, rem;
  var i, j;
  for (var d = 1; d < depth; d++) {
    var level = [];
    var tree = false;
    var n = prior.length * 2;
    if (d + 1 === depth) {
      n = classes;
    } else if (n > width) {
      n = width;
    } else {
      tree = true;
    }
    if (tree) {
      for (i = 0; i < prior.length; i++) {
        j = 2 * i;
        node = makeNode(j, n, d, depth);
        node.id = id++;
        makeEdge(prior[i], node);
        nodes.push(node);
        level.push(node);
        j++;
        node = makeNode(j, n, d, depth);
        node.id = id++;
        makeEdge(prior[i], node);
        nodes.push(node);
        level.push(node);
      }
    } else {
      for (i = 0; i < n; i++) {
        node = makeNode(i, n, d, depth);
        level.push(node);
      }
      rem = prior.slice(0);
      for (i = 0; i < n; i++) {
        node = rem.splice(Math.floor(rem.length * Math.random()));
        makeEdge(node, level[i]);
        j = Math.floor((n - 1) * Math.random());
        if (j === i) {
          j++;
        }
        makeEdge(node, level[j]);
      }
      level = [];
      for (i = 0; i < prior.length; i++) {
        rem = prior[i].children;
        for (j = 0; j < rem.length; j++) {
          node = rem[j];
          if (!node.id) {
            node.id = id++;
            level.push(node);
          }
        }
      }
    }
    prior = level;
  }
  return nodes;
}

function nodeDisplay(d) {
  return d.leaf ? "red" : "blue";
}

function getId(d) {
  return d.id;
}

var duration = 250;

function displayDag(svg, nodes) {
  var root = nodes[0];

  //show root node
  svg.selectAll("g.node")
    .data(nodes[0], getId)
    .select("circle")
      .attr("r", 4.5)
      .style("fill", nodeDisplay);

  //Add children of a node
  function update(source) {
    var node = svg.selectAll("g.node")
      .data(source.children, getId);

    var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .attr("transform", function(d) {
        return "translate(" + source.y + "," + source.x + ")";
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
      .attr("r", 4.5)
      .style("fill", nodeDisplay);

    var edges = source.children.map(function(child) {
      return {
        id: node.id + "-" + child.id,
        source: source,
        target: child
      };
    });

    // Update the links…
    var link = vis.selectAll("path.link")
      .data(edges, getId);

    // Enter any new links at the parent's previous position.
    link.enter().insert("svg:path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        return diagonal({
          source: d.source,
          target: d.source
        });
      })
      .transition()
      .duration(duration)
      .attr("d", diagonal);

    // Transition links to their new position.
    link.transition()
      .duration(duration)
      .attr("d", diagonal);

  }

  //Update each on a timer
  nodes.forEach(function (node, i) {
    setInterval(function() {
      update(node);
    }, duration); 
  });
}
