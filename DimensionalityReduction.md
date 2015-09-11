Dimensionality reduction
=====================

Reducing a dataset in high dimensions down to low dimensions while retaining the important characteristics of the data, by way of a projection.  The most important element is to choose a projection with a high variance (most data encoded) but with fewer features.  

## Principle Components Analysis

The data should be assumed to be centered (mean at origin).  The optimization is therefore max(sum(xu)^2) where ||u||^2 = 1.  Using matrix algebra this is

`max u for ||Xu||^2 where ||u||^2 – 1 = 0`

Each successive dimension can be found with the additional constraint that the vector must be orthogonal to all vectors preceding it.  

The algorithm

1. Compute mean: `u <- mean(X)`
2. Compute covariance matrix: `D <- t(X – u t(1)) * (X-u t(1))`
3. Compute the eigenvalues and vectors and order by the eigenvalues (variance)
4. Truncate the eigenvector matrix to discard the eigenvectors with low variance `U <- top K of D`
5. Convert to the new projection `(X-u1)U`

PCA can also be computed with Singular Value Decomposition.  

Although PCA is a good compression algorithm it is not optimal for classification because it completely ignores the label.  

## Linear Discriminant Analysis

Unlike PCA, LDA does take labels into account. LDA is designed such that the classes are as linearly separable as possible within the constraints of the algorithm.  It gives optimal results if the classes are Gaussian and have equal covariance.  

The LDA algorithm works as follows:

1. Calculate the mean for each feature (global mean) u
2. Split the data by class into separate groups.
3. For each group x<sub>i</sub>:
  1. Calculate prior probability of group (group samples / total samples) p<sub>i</sub>
  2. Calculate mean for each feature (group mean) u<sub>i</sub>
  3. Subtract global mean from group samples x<sub>i</sub><sup>0</sup>
  4. Calculate covariance matrix for group samples c<sub>i</sub>
4. Calculate mean of the group covariance matrices weighted by the prior probability C

This allows you to calculate a discriminant function for a sample z:

f<sub>i</sub> = u<sub>i</sub>C<sup>-1</sup>z<sup>T</sup> - (1/2)u<sub>i</sub>C<sup>-1</sup>u<sub>i</sub><sup>T</sup> + ln(p<sub>i</sub>)

To make a prediction:
1. Calculate the discriminant function for all groups for the example
2. Pick the group with the maximum value

Alternatively, you can use the discriminant functions to calculate a new feature vector, one feature for each group.
