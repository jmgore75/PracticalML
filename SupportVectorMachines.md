Support Vector Machines and Kernel-based algorithms
=================================

Support Vector Machines are a way of solving a linear separation problem that attempts to find a separating hyperplane with as large a margin as possible.  It is set up to optimize the separation.  

SVMs find these solutions not in absolute terms but on the basis of some subset of the samples: which are the _support vectors_.  The key to this is slack parameters.  Slack parameters denote that a point can be moved from one side of the boundary to the other, with penalty.  By introducing one slack parameter for each training example then you can create an optimizable problem.  Any sample with a non-zero slack is a support vector.  

## Kernels

SVMs can also exploit kernels, and popularized the notion of kernelization.  A kernel is just a generalized dot product. If an algorithm can be written so that they only ever depend on kernel products between data points and not on the data points themselves, then it can be kernelized. `K` is a valid kernel if it corresponds to the inner product between two vectors.  The kernel is essentially a measure of similarity between two data points.  

Kernels transform a linear representation of data into a more useful representation, which usually has more or even infinite dimensions.  The features in this transformation can make finding a solution much easier, such as by including combinatorial features or projecting into an orthogonal space.  The trick is that kernels do not have to actually _make_ the transformation in order to solve the optimization problem: a simple corresponding kernel function can be applied within the optimization.  There are many kernel options, but the radial basis function is particularly significant, as it defines smooth, round boundaries around the support vectors.  

Important kernels include:

- Polynomial kernels: `(1+xz)^d`
- Gaussian kernel/Radial basis function: `exp(-gamma || x-z|| ^ 2)`
- Hyperbolic tangent (technically invalid) = `tanh(1+xz)`
- Many others!
- Kernel addition `K(x,z) = K1(x,z) + K2(x,z)`

One-class SVM is a unsupervised technique which only has one set and defines a boundary for it for novelty detection (typically using the radial basis function)
