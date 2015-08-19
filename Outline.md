# A Practical guide to Machine Learning

## XXXX vs models

First some basic terminology:

The ultimate goal of any machine learning task is to generate a model which accurately describes the data and can be used to characterize future data.  

Machine learning comes in two major forms: supervised and unsupervised.  

In supervised learning you are learning a model which when given an input can make an accurate prediction of an output.  
- Classification: predict a categorical value (yes/no)
- Regression: predict a numeric value

In unsupervised learning you are are trying to describe your data.  Fundamentally, this is a sort of compression.
- Cluster the data to identify groups
- Identify patterns and gain insight into commonalities
- Actual data compression

Some supervised algorithms can be used in an unsupervised fashion by simply running them forwards and training them backwards.  This is called autoencoding.  

## The ideal ML algorithm

## The reality

To say that the field of ML is complex is a bit of an understatement.  
- There are dozens of different basic algorithms.  
- Most algorithms have hyperparameters for tuning their performance.  Failure to choose good hyperparameters may mean that your algorithm will fail to train at all.  
- Beyond hyperparameters, many basic algorithms have minor variants to choose from
- Many ML
- The algorithm you choose may require you to preprocess your data (whitening is particularly common with linear algorithms)
-

There are many many different machine learning algorithms, each with their own strengths and weaknesses.  

On top of this, ML all but requires large amounts of data

## Deep Learning



## Bias vs. Variance

A ML algorithm has high intrinsic bias if it preferentially favors certain kinds  of models and cannot learn other types of models efficiently or at all.  

For instance, a decision trees and

## Ensembles, Bagging, and Boosting

Many algorithms .  

Boosting

## What algorithms do I need to know how to use?
- Extremely Randomized Forests
- Deep Neural Networks
  - Fully Connected Layers
  - Convolutional Layers
  - Pooling layers
  - Dropout
  - Activation Functions
    - ReLU
    - Sigmoid/Tanh
    - Nothing!

  - Experimental architectures
    - MaxOut (Pooling)
    - ChannelOut

- Extreme Learning Machines

## Pitfalls
- Impractically large models
-

## Major flavors of Machine Learning
### High intrinsic bias

## Decision Trees
The trick is

## Linear/Logistic
### Solving analytically
Using SVD algorithm

### Solving with Gradient descent
## Layered Approaches
Each layer feeds into the next

The network can be trained through backwards propogation when using an iterative training approach.  

## Major recipes
