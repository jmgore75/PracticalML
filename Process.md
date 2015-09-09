The process of machine learning
=====================

1. Know your problem
2. Know your data (is it text, is it image)
3. Set up your test harness
4. Spot check a variety of algorithms
5. Fine tune the best ones

### Know your problem

The most fundamental question for machine learning (or indeed most projects) is what problem are you trying to solve? Can machine learning help you with this?  What kind of machine learning question is it?

<!-- TODO understanding your problem -->

### Know your data

You must also understand your data and how to use it.

- What data do you have to work with? Is it sufficiently large and with sufficient features?  Are there any other features that you think might be useful and can you get them?
- Where is your data coming from? How will you obtain it? Do you have sufficient privileges?
- Are you legally allowed to use your data to solve your problem? Be especially cautious about patient data.  
- What form is your data in? How will you reformat it to use in your algorithms?  Do you need to do this only once or more often?
- What are the types of your features? Will any of them need to be transformed into a different form for processing?
- Are any of the features in your data identifiers? You may want to discard these: they can be used to overfit, and should not be interpreted as numbers.  

In many if not most cases, the amount of time you spend wrangling your data will exceed the amount of time you spend actually choosing and fitting models.  As trivial as it sounds, you can't train a model without data.  

### Set up your test harness

The main steps are as follows:

1. Wrangle your data (e.g. from text)
2. Preprocess your feature set (remove bad or useless features, engineer new features)
3. Pick performance measure (usually accuracy)
4. Train your models with cross validation and evaluate scores.  For each model:
  1. Scale or whiten your training set, if necessary
  2. Scale or whiten your test set using the parameters that you used on your train set
  2. Train model on your preprocessed training data
  3. Score your preprocessed train and test data with your model and performance measure
5. Evaluate your models
6. Refine your models by choosing new hyperparameters

#### Cross Validation

Cross validation requires you to split your training data you have available to you into two sets, train and cv.  You train with the train set and then evaluate on the cv set.  Because the model you trained knows nothing about the cv set, your cv score is a good indicator about how well your model will perform on future data.  The train score tells you only how well you were able to model the data you trained with.  

To ensure honest cv scores, your preprocessing step should only use the train set.  In other words, do _not_ scale your data set and then pick your train set from that, pick your train set and then scale based on that.  Some machine learning libraries such as scikit-learn provide a Pipeline object, which you can use to combine your preprocessor and model into a single object that behaves like a model for convenience in training and processing.  Other packages may have built-in handling of preprocessing.  

In other circumstances you may want to perform relatively heavy preprocessing such as PCA or LDA on the entire data set, possibly using unlabeled data entirely outside of your training set.  Although this will allow you to evaluate more models in less time and may boost your cv score, it may not be representative of how the model will perform on future unknown data.  

### Spot check a variety of algorithms

I would strongly recommend that you always spot check the following models with the specified parameters

- Extremely Randomized Trees:
- Random Forest:
- Linear or Logistic Regression: (standardized data)
- Neural Networks
  - Extreme Learning Machines (hidden layer with three times as many nodes as features)
  - Basic 1 and 2-layer perceptrons (hidden layers with half as many nodes as features)

### Fine tune your best models

Now that you have some good candidate models, see if you can improve their performance by adjusting their hyperparameters.  Generally you can and should do this using a grid search of hyperparameter combinations, or a randomized search within a certain window.  

#### Evaluating individual models

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

### Go the extra mile

- Try combining your best models as an ensemble and see if that produces a good improvement
- Engineer your initial features and see if that improves your result:
  - Extreme Learning Machine style random non-linear mapping
  - PCA or LDA dimension reduction
