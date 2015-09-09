# A practical guide to applied machine learning

To say machine learning is a big subject is a big understatement - it can be difficult to know where to even begin!  But understanding and applying machine learning may be easier than you think.  

Using python and scikit-learn, we'll walk through a machine learning process from start to finish.  Along the way we'll discuss when to apply machine learning, the most successful algorithms, best practices, and even a bit of philosophy.

# Topic notes

## Steps

- Know your problem
- Know your data (is it text, is it image)
- Set up your test harness
  - Wrangle your data (e.g. from text)
  - Preprocess your data (whitening)
  - Train, test (with cross validation)
  - Pick performance measure (usually accuracy)
- Set up an all-purpose test harness
- Spot check a variety of algorithms
- Fine tune the best ones


- Ensemble your top choices?


## Factors in selecting ML environment (if you have a choice)

1. Plenty of memory (8GB)
2. NVidia GPU installed (for CUDA) or a decent CPU
3. Prefer Linux

First and foremost, you want memory, for the following reasons:
- Datasets themselves are often large
- Many algorithms have significant working memory requirements, particularly when there are many features (SVM, DNN)
- Pretty much all algorithms with low intrinsic bias improve with more data, so if you can get more you should.  

Running models on the GPU rather than the CPU can massively improve their performance: 30 times speedup is often the case.  This can make a huge difference in your ability to investigate.  

The major machine learning/data science platforms are available on all platforms.  However, a lot of ML libraries are high performance and requires compilation (including dynamic compilation).  Naturally the build process makes a lot of assumptions about particular compilers and libraries being available (even the shell environment).  And they are nearly all open source.  So Linux will generally be your least painful option.  OS X is ok but often requires you to set up a lot of stuff in advance.  The windows situation is similar, and additionally complicated by it's non-unix heritage.  

## Strengths and weaknesses of the major ML platforms:

At the moment, there are four major ML environments: R, Python, MatLab, and Julia.  I have used all four environments at one time or another.  Additionally, there are many C libraries, Java libraries, and services available.  

[R](https://www.r-project.org/) is the premier open source statistical computing and graphics language and environment.  It is also the most popular ML toll and has thousands of packages.  It is widely used in academia and research, and implementations of new algorithms are often delivered in R.  

[Python](https://www.python.org/) is a high-level and flexible general-purpose dynamic programming language.  Nearly all machine learning on python goes through the  [scikit-learn](http://scikit-learn.org/stable/index.html) package, which wraps many ML algorithms in a single standard interface along with plenty of processing and analysis tools.  Python is production ready and is excellent for data wrangling.  For these reasons it is my personal choice.  

[MatLab](http://www.mathworks.com/products/matlab/) is a numerical computing environment with extensive use in academic and research institutions.  It is also proprietary and expensive.  Its open source clone [Octave](https://www.gnu.org/software/octave/) uses the same language but is not nearly as nice.  

[Julia](http://julialang.org/) is a very new high-performance dynamic programming language. It is specifically designed for numerical and scientific computing but also aims to be an effective general purpose language: "[the speed of C with the dynamism of Ruby](http://julialang.org/blog/2012/02/why-we-created-julia/)".  In practice the code is most similar to MatLab but with [parametric types](https://en.wikipedia.org/wiki/Parametric_polymorphism).  The performance is actually quite good.  As such it has attracted a lot of interest in the machine learning community and is rapidly developing a package ecosystem.  However it is still early beta and even some core APIs are changing, so I can't recommend it just yet.  


## The algorithms that really matter

Any algorithm could be the right one.  But it will probably be one of two.  

For supervised learning:
- Forests are the best general purpose algorithm, especially when your features are of many different types (e.g. your typical table of data).  They are very forgiving and easy to work with.  
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

##

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
