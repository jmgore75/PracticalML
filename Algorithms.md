The different types of machine learning
======================================

## The algorithms that really matter for supervised learning

There is something called the ["No free lunch theorem"](https://en.wikipedia.org/wiki/No_free_lunch_theorem) in machine learning.  In a nutshell, it implies that no one algorithm will be suitable for all problems and that any algorithm could be the right one.  In practice however, two types of algorithm do [especially well](http://jmlr.csail.mit.edu/papers/volume15/delgado14a/delgado14a.pdf) on a wide range of real-world problems:  

- [Random forests](RandomForests.md) are the best general purpose algorithm, especially when your features are of many different types (e.g. your typical table of data).  They are very forgiving and easy to work with.
- [Neural networks](NeuralNetworks.md) are best for numerical data, especially where your features are fundamentally similar.

If your data has a complex, non-tabular structure, then you have fewer (but more interesting) options.  Two neural networks in particular are worth mentioning:

- [Deep convolutional neural networks](NeuralNetworks.md#deep-neural-networks) are the clear winners for structured numerical features (e.g. image pixels).
- [Recurrent LSTM neural networks](NeuralNetworks.md#recurrent-neural-networks) are the clear winners for processing or producing streams of data (e.g. audio and text)

Also:

- Simple linear algorithms like logistic regression are cheap and often worth a shot.  
- [Support Vector Machines](SupportVectorMachines.md) also perform well and are usually worth testing.  

For unsupervised learning:
- Stacked Autoencoders

For feature selection and engineering:
- PCA
- LDA
- [Random forests](RandomForests.md) have the side benefit of identifying the most useful features

## General

- More training data beats a more efficient algorithm. But scalability is also a concern.  
  - To a first approximation most algorithms produce similar results, even in radically different algorithms.
  - Powerful learners can be accurate but unstable (unreliable and )
- Feature engineering and parameter optimization are absolutely critical and usually the most complex part of the process.  
- Fixed size learners have limits on how accurate they can be, while variable sized learners often fail due to limitations of their algorithm or computational cost.  Clever algorithms often work the best in the end.
- Learners that produce interpretable output (rule sets) can yield useful insights.

## Beyond the basics

Philosophy ahead

## "Extreme" machine learning

We have discussed two "extreme" algorithms: [Extremely Randomized Trees](RandomForests.md#extremely-randomized-trees), a variant on Random Forests, and [Extreme Learning Machines](NeuralNetworks.md#extreme-learning-machines), a variant on neural networks.  Despite having completely different algorithm designs, the "extreme" variants have a fundamental behavior in common: rather than trying to _optimize_ some internal parameter, they instead choose from _many random options_, and thus have _less intrinsic bias_ than their cousins.  

Consequently they are less likely to overfit, are better at picking up on weak signals, and as a side benefit are simpler and faster to train.
