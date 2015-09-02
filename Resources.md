## Overview of machine learning approach
<http://machinelearningmastery.com/machine-learning-for-programmers/>

This is a pretty good article about how to approach machine learning:
* Top-down (objective, not algorithm focused)
* Use a systematic approach to
* guarantee that the end result is good (often more reliable than accurate)
* Tool agnostic

Here's the process:
1. Define problem
2. Prepare data
3. Spot check algorithms
4. Improve results
5. Present results
6. Deploy and Use

Recommended tools
* Weka (graphical, good for one-off)
* Scikit-learn (develop and deploy)
* Deep dive (R caret)

Datasets
* [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/)
* Kaggle
* [KDD Cup](http://www.sigkdd.org/kddcup/index.php)
* Avoid image and text data, too specialized to start

Development tips
* Write up what you did
* Version of course, save to public Repository
* Focus on small data

## The value of Random Forests

Basically random forests have few hyperparameters and require little to no tuning.  They tend to perform very well on heterogeneous data sets and are easy to interpret.  Also, more trees gives you more accuracy - random forests are not prone to overfitting!  Extremely Randomized Trees are arguably the best approach (citation?).  

Author advocates spot checking a dozen or so algorithms and then focusing on the ones that perform well.  So you need a good test harness.  All well and good, but _how_ do you identify the algorithm to settle on.

<http://machinelearningmastery.com/use-random-forest-testing-179-classifiers-121-datasets/>

Also, Decision Jungles are low-memory generalizations of random forests

<http://geekstack.net/resources/public/downloads/tobias_pohlen_decision_jungles.pdf>

## Caret Package
R package that handles model creation, discovery, and tuning

<http://machinelearningmastery.com/caret-r-package-for-applied-predictive-modeling/>
