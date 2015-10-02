Development Notes
===========

# Review Notes

Clean up notes

Interlude to explain concept of validation
  Also bias-variance as source of error

##

https://medium.com/@alevitale/notes-from-deep-learning-summit-2015-london-day-1-1599f603a40b

<http://www.pyimagesearch.com/2014/09/22/getting-started-deep-learning-python/>

Need To:

http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html

http://scikit-learn.org/stable/modules/learning_curve.html

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
