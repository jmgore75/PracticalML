# A practical guide to applied machine learning

- To say machine learning is a big subject is a big understatement



- Know your problem
- Know your data (is it text, is it image)
- Set up your test harness
  - Transform your data (e.g. from text)
  - Preprocess your data (whitening)
  - Train, test (with cross validation)
  - Pick performance measure (usually accuracy)
- Set up an all-purpose test harness
- Spot check a variety of algorithms and pursue
- I'll be using Python's scikit-learn and nolearn


- In my experience
  - Neural networks are best for numerical data, especially homogenous data
  - Convolutional layers are a necessity for data with structure (i.e. images)
  - Forests work best for



<http://www.pyimagesearch.com/2014/09/22/getting-started-deep-learning-python/>

- Using ML to learn from your data
  - Using forests and dimension reduction to identify your important variables

- Starting algorithms
  - Extremely randomized trees
  - PCA
  - Logistic regression
  - Neural Networks
    - Extreme Learning Machines
    - Basic 1 and 2-layer
    - Convolutional input

- Technical
  - Preprocessing data (whitening)
  - Keeping track of your progress
  - Layering
  - Ensembles

- Conceptual
  - Machine Learning vs. statistics
  - Supervised and Unsupervised
  - The human element in the ML process
  - Any algorithm could be the right one - but it will probably be one of these
  - Big data, small data, and expanded data
  - Dealing with bias in your training set
  - Catastrophic forgetting
  - ML on small hardware
  - The value of a good API

- Touch on
  - Choice of language and environment
  - Dataframes are useful but non-essential
  - What you need to understand before delving deeper (matrix algebra + tools)
  - Highly recommended learning resources (blogs and courses)
  - External dependencies (often designed for linux, can be applied to os x with difficulty, rarely designed for windows)
  - Using your gpu (often hard to set up but totally worth it)
  - Cloud computing (attractive model but it will add up)
  - Batch and online algorithms
  - Exciting algorithms

- Ways to use Machine Learning
  - To model and predict (of course)
  - As a way to narrow down parameters or the search space before applying a more exhaustive algorithm
  - As a way to explore the importance of features of your data (using forests)
  - As a generic control vs. non-machine learning models

- Feature selection and feature engineering

- You should save the following attributes for every model you reduction.  Store to disk as pickle or database.  
  - Enough information to recreate a similar model
    - Model class
    - Model / library version
    - Model parameters
    - A hash or repl of all of the above
    - You do NOT need to store the entire model, which can be quite large!
    - version of train/test data
  - Model performance (have columns for all of the following)
    - Performance measure
    - Training time
    - Number of iterations
    - CV/test accuracy
  - Meta
    - Timestamp

Go through some tables from different data sets to demonstrate what models rise to the top.  
