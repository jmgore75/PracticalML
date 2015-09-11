External resources
====================

## Articles

### Machine learning checklist

<http://machinelearningmastery.com/machine-learning-checklist/>

Nice article going over everything you should do

> Often you don’t need the very best solution. In fact the very best solution may be what you don’t want. It can be expensive to find, it can be fragile to perturbations in the data and it may very likely be a product of over fitting.

> You want a good solution, that is good enough for the specific needs of the problem that you are working on. Often a good enough solution is fast, cheap and robust. It’s an easier problem to solve.

### The value of Random Forests

Review: <http://machinelearningmastery.com/use-random-forest-testing-179-classifiers-121-datasets/>

Original: <http://jmlr.csail.mit.edu/papers/volume15/delgado14a/delgado14a.pdf>

Contends that random forests are the best overall algorithms.  This reference was an exhaustive study of 179 classifiers over 121 data sets, giving 21,659 combinations classifier-data set over all the families they could think of.  They tested a variety of implementations of the algorithms in R, C, Weka, and Matlab.  They did only standard scaling on the data.  Average accuracy ranged from 82% to 49.2%.

The top ranks were dominated by Random Forests, then SVM, followed by Neural Nets.  
- 1, 2, 5: Random forests
- 3: Gaussian SVM using LibSVM (1v1 for multiclass)
- 4: Polynomial SVM
- 6: Gaussian kernel ELM
- 7, 8: Radial SVM
- 9: C5.0 (Boosting ensemble)
- 10: avNNet (Committee of 5 Multi layer perceptrons with 1, 3, or 5 hidden neurons)

Interesting bits:
- Random Forest had an average accuracy only 4.9% less than the maximum accuracy.  
- For 84.3% of the tests the parRF algorithm achieves at least 90% of the maximum accuracy
- Figure 2 right: Shows best random forest vs. the maximum accuracy - it does
- ELM with a gaussian kernel was the best neural net, which is interesting because ELM is such a simple approach.  It also had the highest probability of maximum accuracy, although a relatively low rate of 95% maximum accuracy (i.e. less reliable than the others).
- For MLP uses #hidden neurons equal (#inputs + #classes)/2
- Figure 5: Twenty classifiers with the highest percentages of the maximum accuracy. MAB means MultiBoostAB, BG means Bagging.
- Figure 6 top: Friedman rank interval for the classifiers of each family

Top approaches:

> parRF_t uses a parallel implementation of random forest using the randomForest package with mtry=2:2:8.

> rf_t creates a random forest using the caret interface to the function randomForest in the randomForest package, with ntree = 500 and tuning the parameter mtry with values 2:3:29.

> svm_C is the support vector machine, implemented in C using LibSVM (Chang and Lin, 2008) with Gaussian kernel. The regularization parameter C and kernel spread gamma are tuned in the ranges 2<sup>−5</sup>..2<sup>14</sup> and 2<sup>−16</sup>..2<sup>8</sup> respectively. LibSVM uses the one-vs.-one approach for multi-class data sets.

> elm_kernel_m is the ELM with Gaussian kernel, tuning the regularization parameter and the kernel spread with values 2<sup>-5</sup>..2<sup>14</sup> and 2<sup>-16</sup>..2<sup>8</sup> respectively.  Neurons between 3 and 200. From Huang et al.  

> C5.0_t creates a Boosting ensemble of C5.0 decision trees and rule models (function C5.0 in the hononymous package), with and without winnow (feature selection), tuning the number of boosting trials in {1, 10, 20}

> avNNet_t, from the caret package, creates a committee of 5 MLPs (the number of MLPs is given by parameter repeat) trained with different random weight initializations and bag=false. The tunable parameters are the #hidden neurons (size) in {1, 3, 5} and the weight decay (values {0, 0.1, 10<sup>−4</sup>}). This low number of hidden neurons is to reduce the computational cost of the ensemble.

## Online courses

### Andrew Ng's Machine Learning course on Coursera

<https://www.coursera.org/course/ml>

Probably the definitive massive online open course (and one of the first), and still one of the best for learning machine learning.  It covers several major types of algorithm and gives you a firm grounding in the bias-variance tradeoff.  If you want to implement something from scratch this is a great place to start.  Exercises are all in Matlab.  

- Supervised
  - Linear algorithms
  - Neural networks
  - Support vector machines
- unsupervised
  - Dimensional reduction
- Best practices
  - Bias-variance theory
  - Performance analysis

I should note that I find the video lecture format of online courses to be a very slow way to learn.  I find text with copious code examples to be far better.  However, video courses are often the best thought out and complete.  So to speed things up, try increasing the playback speed.  

### Overview of machine learning approach

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

## Machine learning packages

### Caret Package (R)
R package that handles model creation, discovery, and tuning

<http://machinelearningmastery.com/caret-r-package-for-applied-predictive-modeling/>
