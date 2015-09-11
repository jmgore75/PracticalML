Geometric view of data
==================

Each input datum is often treated as a list of features, and you have a list of data.  This suggests a geometric view of the data, where we have one dimension for every feature.  Examples are then just points in a high-dimensional space.  A data point is therefore represented by a feature vector.  

Many geometric operations can then be performed on this data.  In particular, it favors a nearest neighbor model of learning, where proximity in the space equates to predictive potential.  

- The dimensionality can be extremely high for many problems.  
- The distance will differ depending on your feature scale.  
- Decision boundaries are hyperplanes between groups of points to establish classification boundaries.  
- Clustering generally requires a geometric view of the data.  

## Distance

Euclidian distance is the most common metric but not always the most appropriate one.  Euclidian distance is calculated as `sqrt(sum((xn-yn)^2))`.

Discrete variables often benefit from a different distance measure, such as Hamming distance.  Hamming distance is equal to the count of the number of substitutions necessary to turn one string into another (it is also known as the overlap metric).

Often, a feature weight should be applied prior to calculating distance.  Pseudometrics such as Largest Margin Nearest Neighbor or Neighborhood Components Analysis may also be justified.

## Problems with high dimensional data

Firstly, comparing positions against a large number of points (as one would do in k-means or KNN) is computationally expensive.  Indexing the data into a grid can help with that, but with even less than 20 features the indexing cells become huge.  

Secondly, the distance between random points in a bounded high dimensional space [tends to be the same](http://yaroslavvb.com/papers/koppen-curse.pdf).  More formally, the maximum Euclidian distance between two points in a D dimensional unit cube will be `sqrt(D)` and the average will approach `sqrt(D/6)` with high `D`, but the variance will remain the same.  Since we would normalize by dividing by the max distance, normalized variance decays to zero with an order of `sqrt(1/D)`.  Similar behavior can be described for `D` dimensional balls or other bounded spaces – in fact, the ratio of the volume of a hypersphere to its embedding hypercube goes to 0 by the order of n!.

This can be attributed to the law of large numbers - each dimension added will tend to push the aggregate value (distance) towards the mean.  Statisticians will thus sometimes describe high dimensional space as "spiky", with the majority of the volume concentrated in the inner part. You could also say that with increasing dimensions probabilities become reliabilities.  Features in random patterns (such as textures) are a unique property of low dimensional space.

However, useful data is not random and generally has [lower true dimensionality](DimensionalityReduction.md) than the ones it is expressed in.  So real data does not necessarily suffer from this problem.  
