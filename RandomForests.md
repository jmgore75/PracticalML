Decision Trees and Random Forests
====================

A random forest is simply an ensemble of specially constructed decision trees.  

## Decision Trees

Decision trees are arguably the simplest and most intuitive machine learning model in existence.  They are essentially a flowchart: for each node starting at the root, you evaluate a rule and are directed to another node, until you reach a final decision.  

Training nodes in a decision tree has the following steps:
1. Start with your current data set
2. If your data set has only one output class, then create a leaf node specifying the class
3. Otherwise create a decision node:
  1. Find the best rule to split one of your features
  2. Split your data with the rule
  3. Repeat the node training process with each of the data splits

Most machine learning algorithms will require you to preprocess your data by converting it to a numeric form and often scaling it to a tractable range.  Decision trees are an exception: the features can be categorical, discrete, or continuous in any range.  

A decision tree can describe any given set of data almost perfectly if allowed sufficient depth.  Consequently, they have a bad tendency to overfit in a way that is difficult to avoid.  

A decision tree only ever considers one feature at a time. It cannot model mathematical relationships between features, and thus cannot generalize well to border cases.  Plotting the map of a decision tree is disturbingly square.  

## Random forests

As I said before a random forest is simply an ensemble of specially constructed decision trees.  What makes it random is how the trees are constructed.  If you used the conventional decision tree algorithm every tree would look the same.  Random forests use two main tricks that ensure that every tree is different:

1. Instead of using the full data set for each tree each training set is bootstrapped: sampled with replacement from the original data.  So each tree gets its own training set which may have duplicates but has a distribution similar to the whole set.  When evaluating the model as a whole, the results from the individual trees will be aggregated.  Bootstrapping and aggregating in combination is known as [bagging](https://en.wikipedia.org/wiki/Bootstrap_aggregating).  
2. Bootstrapping alone is not enough to ensure that trees will be sufficiently different from each other, so when making a branch the algorithm will look at only a random subset of features rather than all features.  

Random forests have several really nice practical aspects:

- Since they are based on decision trees, no preprocessing of features is necessary.  
- There are few parameters to tune and those parameters are very forgiving.  Essentially it's just the maximum depth, number of features to sample, and the number of trees.  
- Training forests is an embarassingly parallel problem, and is typically quite fast.  You can add or remove new trees to forests without retraining the existing trees.  Evaluation is also reasonably fast.  

Most importantly random forests work very well on a very large number of problems.  In fact with random forests you can continue adding trees to improve your accuracy without danger of overfitting.  This is because [bagging is most effective on unstable algorithms that overfit easily](http://statistics.berkeley.edu/sites/default/files/tech-reports/421.pdf)... and decision trees overfit more easily than just about anything.

## Extremely Randomized Trees

Extremely Randomized Trees are a variant of random forests.  To create a decision branch in a conventional random forest, the algorithm will pick a random set of features and find the best split.  The Extremely Randomized Trees variant will go one step further and randomize both features and their _splits_, and pick the combination that works best.  

The splits are therefore less correlated than they would be in Random Forests, which helps produce smoother boundaries in the aggregate.  In practice, extremely randomized trees often give better results than conventional random forests.  More on this later.  

## Decision Jungles

Decision trees grow exponentially with depth, which can be a problem in constrained environments.  Microsoft has developed a variant of random forests called [decision jungles](http://research.microsoft.com/apps/pubs/?id=205439) which use directed acyclic graphs instead of trees.  The number of nodes in a level is generally constrained, so the DAG will grow only linearly past a certain point.  A DAG thus reduces redundancy commonly found in trees.  They are more complicated to train but generally require less memory to store.  Also, they are also less prone to overfitting and generalize better.  

Fun fact: the invention of decision jungles at Microsoft was probably prompted by the XBox Kinect controller, which famously uses random forests.  

## Interesting notes

- More predictors in an ensemble means better accuracy, but there are diminishing returns.  As a practical matter you should evaluate a range of ensemble sizes and pick the smallest size that is acceptably accurate and/or the largest size that fits within your constraints.  At runtime, you can produce a less accurate result faster and with less effort by evaluating fewer predictors.  
