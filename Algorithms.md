The different types of machine learning
======================================

## The algorithms that really matter for supervised learning

There is something called the ["No free lunch theorem"](https://en.wikipedia.org/wiki/No_free_lunch_theorem) in machine learning.  In a nutshell, it implies that no one algorithm will be suitable for all problems and that any algorithm could be the right one.  In practice however, two types of algorithm do especially well on a wide range of real-world problems:  

- Random Forests are the best general purpose algorithm, especially when your features are of many different types (e.g. your typical table of data).  They are very forgiving and easy to work with.
- Neural networks are best for numerical data, especially where your features are fundamentally similar.

If your data has a complex, non-tabular structure, then you have fewer (but more interesting) options.  Two neural networks in particular are worth mentioning:

- Deep convolutional neural networks are the clear winners for structured numerical features (e.g. image pixels).
- LSTM neural networks are the clear winners for processing or producing streams of data (e.g. audio and text)

Also:

- Simple linear algorithms like logistic regression are cheap and often worth a shot.  
- SVM also performs well and is usually worth testing.  

For unsupervised learning:
- Stacked Autoencoders

For feature selection and engineering:
- PCA
- LDA
- Random Forests have the side benefit of identifying the most useful features

## Decision Trees and Random Forests

A random forest is simply an ensemble of specially constructed decision trees.  

### Decision Trees

Decision trees are arguably the simplest and most intuitive machine learning model in existence.  They are essentially a flowchart: for each node starting at the root, you evaluate a rule and are directed to another node, until you reach a final decision.  

Training nodes in a decision tree has the following steps:
1. Start with your current data set
2. If your data set has only one output class, then create a leaf node specifying the class
3. Otherwise create a decision node:
  1. Find the best rule to split one of your features
  2. Split your data with the rule
  3. Repeat the node training process with each of the data splits

Most machine learning algorithms will require you to preprocess your data by converting it to a numeric form and often scaling it to a tractable range.  Decision trees are an exception: the features can be categorical, discrete, or continuous in any range.  

A decision tree can describe any given set of data perfectly if allowed sufficient depth.  Consequently, they have a bad tendency to overfit in a way that is difficult to avoid.  

A decision tree only ever considers one feature at a time. It cannot model mathematical relationships between features, and thus cannot generalize well to border cases.  Plotting the map of a decision tree is disturbingly square.  

### Random forests

As I said before a random forest is simply an ensemble of specially constructed decision trees.  What makes it random is how the trees are constructed.  If you used the conventional decision tree algorithm every tree would look the same.  Random forests use two main tricks that ensure that every tree is different:

1. Instead of using the full data set for each tree each training set is bootstrapped: sampled with replacement from the original data.  So each tree gets its own training set which may have duplicates but has a distribution similar to the whole set.  When evaluating the model as a whole, the results from the individual trees will be aggregated.  Bootstrapping and aggregating in combination is known as [bagging](https://en.wikipedia.org/wiki/Bootstrap_aggregating).  
2. Bootstrapping alone is not enough to ensure that trees will be sufficiently different from each other, so when making a branch the algorithm will look at only a random subset of features rather than all features.  

Random forests have several really nice practical aspects:

- Since they are based on decision trees, no preprocessing of features is necessary.  
- There are few parameters to tune and those parameters are very forgiving.  Essentially it's just the maximum depth, number of features to sample, and the number of trees.  
- Training forests is an embarassingly parallel problem, and is typically quite fast.  You can add or remove new trees to forests without retraining the existing trees.  
- Evaluation is also reasonably fast, although naturally slows with the depth and number of trees.  
- Like most ensembles, forests scale well both in training and runtime.  

Most importantly random forests work very well on a very large number of problems.  In fact with random forests you can continue adding trees to improve your accuracy without danger of overfitting.  This is because [bagging is most effective on unstable algorithms that overfit easily](http://statistics.berkeley.edu/sites/default/files/tech-reports/421.pdf)... and decision trees overfit more easily than just about anything.   

### Extremely Randomized Trees

Extremely Randomized Trees are a variant of random forests.  To create a decision branch in a conventional random forest, the algorithm will pick a random set of features and find the best split.  The Extremely Randomized Trees variant will go one step further and randomize both features and their _splits_, and pick the combination that works best.  

The splits are therefore less correlated than they would be in Random Forests, which helps produce smoother boundaries in the aggregate.  In practice, extremely randomized trees often give better results than conventional random forests.  More on this later.  

### Interesting notes

- More predictors in an ensemble means better accuracy, but there are diminishing returns.  As a practical matter you should evaluate a range of ensemble sizes and pick the smallest size that is acceptably accurate and/or the largest size that fits within your constraints.  At runtime, you can produce a less accurate result faster and with less effort by evaluating fewer predictors.  
- Decision trees grow exponentially with depth, which can be a problem in constrained environments.  Microsoft has developed a variant of random forests called [decision jungles](http://research.microsoft.com/apps/pubs/?id=205439) which use directed acyclic graphs instead of trees.  The number of nodes in a level is generally constrained, so the DAG will grow only linearly past a certain point.  A DAG thus reduces redundancy commonly found in trees.  They are more complicated to train but generally require less memory to store.  Also, they are also less prone to overfitting and generalize better.  (Fun fact: the invention of decision jungles was probably prompted by the XBox Kinect controller, which famously uses random forests)

## Neural networks

By stacking layer upon layer, very complex transformations of the data can be described.  

The core neural network architecture is highly flexible.  

## Perceptrons

The most basic form of neural network has been around since 19XX, and is called a perceptron.  

## Deep Neural Networks

It has been mathematically demonstrated that one hidden layer, if sufficiently wide, can approximate any function.  However, multiple layers can approximate many functions much more efficiently.  Deep neural networks are all.  

The historical catch was that due to an issue called gradient ???, the error could not be propogated more than a few of layers and thus deep neural networks could not be trained effectively.  Recently however there have been a series of innovations that have solved that issue.  The chief obstacle to deep learning now is mainly computational power.    

## Convolutional Layers

Many features sets have an intrinsic structure or relationships.  Consider a black-and-white image.  It is fundamentally a collection of pixels.  The pixels are all similar to each other - they can take a value in the same range.  Pixels also have a defined neighborhood of other pixels.  

Generally speaking, if every feature is the same kind of thing, and every feature has a similar set of relationships to other features, then you have conditions necessary to leverage convolutional .  

then convolutional layers are a must.  

## LSTM Recurrent neural networks

Not data to be processed takes the form of independent records.  You may be consuming and/or producing streams of data, such as audio, video, and text.  In that case, the length of the stream may be of unknown size or even indefinite, and how the data changes over time is of fundamental importance.  Your model must therefore possess memory.  

Recurrent neural networks are one of the few documented ways of modeling such data, by allowing state to carry over between steps.  There are many such architectures, but the one most commonly used is the [Long Short-Term Memory](https://en.wikipedia.org/wiki/Long_short_term_memory) architecture.  As RNNs go it is relatively simple but can remember state for an arbitrary length of time.  

- Deep convolutional neural networks are the clear winners for structured numerical features (e.g. image pixels).
- LSTM neural networks are the clear winners for processing or producing streams of data (e.g. audio and text)



### Extreme Learning Machines

Extreme Learning Machines are a variant of neural networks (usually with one relatively large hidden layer).  The input-hidden weights are initialized randomly (like usual).  The hidden-output weights are then calculated analytically (not like usual).  And that's it - no backpropagation necessary.  Amazingly, this comically simple and fast approach works pretty well.  In practice a few rounds of backpropagation will improve the results even more.

Essentially, an extreme learning machine is just a logistic/linear regression, albeit on a random and non-linear transformation of the original features.  The fact that it works, and works well, shows that discovering features (through transformation or engineering) is _the_ critical task of any machine learning pipeline.  

## Support Vector Machines

Handle high-dimensional (lots of features) well

## Beyond the basics

Philosophy ahead

## "Extreme" machine learning

We have discussed two "extreme" algorithms: Extremely Randomized Trees, a variant on Random Forests, and Extreme Learning Machines, a variant on neural networks.  Despite having completely different algorithm designs, the "extreme" variants have a fundamental behavior in common: rather than trying to _optimize_ some internal parameter, they instead choose from _many random options_, and thus have _less intrinsic bias_ than their cousins.  

Consequently they are less likely to overfit, are better at picking up on weak signals, and as a side benefit are simpler and faster to train.
