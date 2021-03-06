The process of machine learning
=====================

1. Know your problem
2. Know your data (is it text, is it image)
3. Set up your test harness
4. Spot check a variety of algorithms
5. Fine tune the best ones

## Know your problem

The most fundamental question for machine learning (or indeed most projects) is what problem are you trying to solve? Can machine learning help you with this?  What kind of machine learning question is it?

- What problem are you trying to solve?
- Is machine learning a good fit for this problem?
  - Is this a supervised or unsupervised question?
- Should you use an existing simple model instead?

### Key data concepts

**Items** are the individual things which you will be learning from or processing.  **Records**, **Points**, or **Samples** are equivalent terms with slightly different connotations.  

**Features** are the distinct traits associated with each item.  **Labels** are what you are attempting to predict for each item.  **Classes** are the discrete possible values which labels may take in classification problems.  

**Models** are the tools you use to explain your samples.  In machine learning, models are built on, and generated by, **Algorithms**.  ML models can have radically different designs but all are intended to learn complex representations of arbitrary data.  The tunable parts of a model are called **Parameters**.  There are also **Hyperparameters** which control how the model is constructed and trained.  Different hyperparameters can produce radically different models.  **Ensembles** are models which are built out of simpler models.  

**Bias** is the tendency of an model to favor specific representations of the data.  Models with high bias will tend to **underfit** the data during training, because the algorithm is incapable of either finding the correct internal representation or representing the data distribution at all.   All algorithms have bias of one form or another, and thus some algorithms will be better suited to some data sets.

**Variance** is the tendency of an algorithm to find very different representations for small variations in the data.  It is the counterpart to bias.  A model with high variance may fail to **generalize** the data and **overfit** it instead, by simply memorizing the samples.  

### Bias-variance tradeoff

Underfitting and overfitting are a common problem.  In underfitting you fail to take information into account.  In overfitting you have encoded the idiosyncrasies of the training data into your solution.  In the worst case your overfit model may be even worse than guessing.  

The tradeoff may be thought of as between bias and variance.  Bias is a measure of accuracy – whether your model match reality or consistently deviates from it.  Variance is a measure of precision – whether your model produces consistent results.  If you were shooting at a target, your bias would be whether your shots were centered on the bullseye, and your variance would be whether your shots were tightly clustered or not.  Underfitting suffers from high bias, because you have lost/averaged away important data.  Overfitting suffers from high variance, because you are too dependent on the example data.  

It is important not to favor bias over variance or vice versa.  Both are relevant.  Unlike bias, variance can generally be compensated for with more data.  

![Learning curve](img/learning.png)

A general technique to reduce variance is bagging (bootstrap aggregating) and resampling.  Numerous replicates of the original data set are made using random selection and replacement.  Each set is used to construct a model and the models are gathered into an ensemble and their results averaged.  [Random Forests](RandomForests.md) are one such approach.  

Variance increases and bias decreases with model complexity.  The goal is to minimize total error.  The sweet spot is where the increase in bias equals decrease in variance.  Unfortunately there is no analytical way to find this point, and you must instead explore the data and choose the level that minimizes the error.  You must have an accurate error measure for this.  Generally resampling based measures are the best way to go about this.  

![Balance bias and variance](img/validation.png)

The inclusion of unrelated features when building a model will basically always hurt your model.  Even relevant features can increase error if the noise is too high.  In practice it is therefore easier to prevent underfitting than overfitting, and thus minimizing true error.  

For detailed dive on this topic, see [Scott Fortman-roe's essay](http://scott.fortmann-roe.com/docs/BiasVariance.html).  

### Main types of learning

There are four major types of machine learning problems:

- Supervised: make predictions
  - Classification: predict from a sample of labels
  - Regression: predict a numeric value
  - Ranking: predict an order for data
- Unsupervised: identify structure
  - Clustering: find groups within your data
  - Density estimation: identify distribution of samples in the feature domain
  - Pattern identification: identify common patterns
  - Representation learning: describe the data with much less information
- Semi-supervised: supervised learning with additional unlabeled data to help characterize the feature domain
- Reinforcement learning: data is generated by interaction with environment, attempting to maximize a reward

### Data and models

The most common form of machine learning problem is to make a prediction for independent samples, where the features of the sample are not really related to each other.  But this is not always the case.  There are many others that require special formulation and considerations, such as:

- [Graphical models](Probabilistic.md#graphical-techniques): Given samples for a collection of nodes, construct a network between the nodes
- [Sequential or process models](NeuralNetworks.md#recurrent-neural-networks): When the input and/or output is a sequence of arbitrary length
- [Structured data](NeuralNetworks.md#convolutional-layers): When there is a structural relationship between the features (such as pixels in an image)

![Structured data](img/diags.jpeg)

## Know your data

You must also understand your data and how to use it.

- Where is your data coming from?
  - How will you obtain it?
  - Do you have sufficient privileges?
  - Are you legally allowed to use your data to solve your problem? Be especially cautious about patient data.  
- What form is your data in?
  - How will you wrangle it into a form that can be analyzed?
  - Do you need to wrangle your data only once or more often?
  - What are the types of your features?
  - Will any of them need to be transformed into a different form for processing?
- What does your data look like?
  - Can you plot it and if so, is their a pattern?
- What data do you have to work with?
  - Do I have enough examples to train with?
  - Do you have many more samples than features? If not training may not be effective.  
  - Do you have a lot of irrelevant features? These can introduce spurious correlations.  
  - Are there any other features that you think might be useful and can you get them?
  - Is it labeled, and if so how?
  - Are your labels balanced?
  - Are any of your features exponential in nature? You may want to log transform them.  
  - Are any of the features in your data identifiers? You may want to discard these: they can be used to overfit, and should not be interpreted as numbers.  

![Data features](img/histograms.png)

## Set up your test harness

The main steps are as follows:

1. Wrangle your data (e.g. from text)
2. Preprocess your feature set (remove bad or useless features, engineer new features)
3. Pick performance measure (usually accuracy)
4. Spot check models with cross validation and evaluate scores.  

### Data wrangling

Data wrangling (or munging or preparation) is widely considered to be the hardest, most complicated part of ML.  There are many aspects of this problem:

  - May come in a wide variety of formats
  - May be messy and include missing data
  - May include unimportant data
  - May be too large for memory, requiring special techniques to process

In many if not most cases, the amount of time you spend wrangling your data will exceed the amount of time you spend actually choosing and fitting models.  As trivial as it sounds, you can't train a model without data.

### Performance measure

If `y` is the truth and `x` is the prediction, you can have a loss function:
- Regression: `(y-x)^2 or |y-x|`
- Classification: `0 if x == y else 1`

This can be combined with the data generating distribution such that:
- Expected loss = `sum(p(x,y)*l(y,f(x)))`
- Training error = `(1/N) * sum(l(y, f(x))`

### Cross Validation

Cross validation requires you to split your training data you have available to you into two sets, train and cv.  You train with the train set and then evaluate on the cv set.  Because the model you trained knows nothing about the cv set, your cv score is a good indicator about how well your model will perform on future data.  The train score tells you only how well you were able to model the data you trained with.  

There are no hard-and-fast guidelines about how train and test splits should be made, what the relationship of the splits should be, or whether to use the same splits on all models.  Cross-fold validation (splitting your data into 3 or more equal sized sets, and test with each one while training with the others) is a popular approach.  The larger the number of folds, the more accurate your aggregate score will be (the extreme case is leave-one-out, where you do this for each individual data point).  Generally during model exploration I prefer to test 1-3 80/20 random splits, and add more if I decide to investigate further.  This seems to work fine.  

### Preprocessing

Most algorithms are only capable of processing numeric values.  Therefore any non-numeric features must be converted:

- Binary features are usually converted to 0 and 1.  
- Categorical features with N values generally should be expanded to N binary features.  This is known as one-hot encoding.  
- Text features are either discarded, treated as categorical features, or otherwise converted to a numeric representation.  It depends on the circumstances.  

Several algorithms (including all the linear ones) require features in models to have similar distributions.  This usually means they are standardized (equal means and equal variances) or restricted to a range (usually (0, 1) or (-1, 1)).  However, such scaling ensures that all features will have equal relevance.  If your features already are scaled meaningfully compared to each other (important features are bigger), then scaling may actually hurt your ability to generate a good model.  

Other models perform optimally with whitening: not only scaled, but features should not correlate with each other.  In those cases, you may need to apply more complicated algorithms such as PCA or LDA.  

To ensure honest cv scores, your preprocessing step should only use the train set.  In other words, do _not_ scale your data set and then pick your train set from that, pick your train set and then scale based on that.  So for each model you will need to:

1. Scale or whiten your training set, if necessary
2. Scale or whiten your test set using the parameters that you used on your train set
2. Train model on your preprocessed training data
3. Score your preprocessed train and test data with your model and performance measure

In other circumstances you may want to perform relatively heavy preprocessing such as PCA or LDA on the entire data set, possibly using unlabeled data entirely outside of your training set.  Although this will allow you to evaluate more models in less time and may boost your cv score, it may not be representative of how the model will perform on future unknown data.  

Some machine learning libraries such as scikit-learn provide a Pipeline object, which you can use to combine your preprocessor and model into a single object that behaves like a model for convenience in training and processing.  Other packages may have built-in handling of preprocessing.  

### Dealing with data bias and error

In many cases the data may be biased towards one label versus the others.  This can skew your error score, as poorly represented classes will get lost in the shuffle and the algorithm will fail to generalize on them.  In the worst case, simply guessing the most common label can give a deceptively high accuracy, without meaningfully fitting the data at all.  

Always check your labels to determine if there is a strong bias towards any of them.  If so, there are different ways of dealing with this. Pick the means that best suits your needs and capabilities:

- Using an alternative error metric
- Subsampling or oversampling to generate an unbiased data set
- Weighting the examples, if your algorithm allows it.
- Pseudo-oversampling with weighted copies

### Dealing with large data sets

Memory is often a bottleneck.  The data itself may be too big to hold at once, or the algorithm may have large internal memory requirements.  This is particularly true for linear algorithms, which are implemented in terms of matrix transformations.  There are a number of tricks to deal with this issue.  

#### Stochastic optimization

Stochastic optimization thinks of training data as a distribution over examples.  Drawing from this distribution is random sampling from your data set.  

This is the key concept behind bagging, but it can also be used in gradient descent. This is called stochastic gradient descent, and typically is done on 1 or 10 points. Step size is very important in this case – stochastic gradient descent is much more sensitive to learning rate than conventional gradient descent.

For really big data, selecting points at random or running through a permutation of the data can be problematic, particularly if the data is too big for memory.  

#### Feature Hashing

Feature hashing reduces the footprint of linear models with only small loss of accuracy.  The idea is to replace features with hashed versions, reducing space from D-many to P-many weights (with P the range of the hash function).  Hash d to get p, then set Xp = Xp + xd. There will be collisions, in which multiple different features are combined into one.  Hopefully the algorithm can handle the noise, and in fact this works pretty well, since some features are appropriately paired and other features the noise balances out.  

### Algorithms to spot check

I would strongly recommend that you always spot check the following models with the specified parameters

- Extremely Randomized Trees:
- Random Forest:
- Linear or Logistic Regression: (standardized data)
- Neural Networks
  - Extreme Learning Machines (hidden layer with three times as many nodes as features)
  - Basic 1 and 2-layer perceptrons (hidden layers with half as many nodes as features)

![Algorithms](img/algorithms.png)

## Evaluating your models

- If your train score is good but your test score is poor
  - You are overfitting.  Adjust your model parameters to try to generalize better.  
- If your train and test scores are poor, then your model is not fitting for any one of the following reasons:
  - Try different hyperparameters.
  - Your model may not have yet converged.  Train for more iterations, and see if it is improving.  
  - The intrinsic bias of your model may be poorly suited to the form of your data.  Try different models.  
  - The features you are working with are not good.  
  - The data you are trying to train with may be of poor quality and it is not possible to generate a good model on top of it (garbage in, garbage out).  Examine your data and see if you need to perform any preprocessing or correction on any of the features.  
- If you are running out of memory or your computer is excessively hot or your hard drive is noisy (indicating paging of memory from disk to RAM)
  - Your model may not handle large numbers of features well.  Try reducing your features and see if that helps.  
  - Your model may not handle large numbers of samples well.  Try training your algorithm in batches (if possible), or reduce the batch size.
  - You may be trying to process more data than your system can handle.  Try buying or using a system with more RAM.
- If your model fails to train at all, or is training very slowly or poorly:
  - Verify that your input was preprocessed in the form required by the model
  - One of your hyperparameters may be be making your model diverge.  Try different hyperparameters.

## Refining your models

Now that you have some good candidate models, see if you can improve their performance by adjusting their hyperparameters.  Generally you can and should do this using a grid search of hyperparameter combinations, or a randomized search within a certain window.  

If your models are nowhere near as good as you think they could be, try performing some feature engineering and see if that improves the result.  Most algorithms do not generate products of features, which can greatly improve models in some instances.  You can help this along by introducing combinatorial features (products of two or more features).  Alternatively, in linear algorithms you can log-transform features: since the sum of logs is equal to the log of products, products and exponents can be discovered.  

- Extreme Learning Machine style random non-linear mapping
- PCA or LDA dimension reduction

### Super learners

If you have multiple models that perform well, you can combine their output predictions weighted by their cross-validation accuracy.  The result will probably better than the sum of its parts.  
