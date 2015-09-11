Linear models and techniques
===========================

A linear equation is one in the form:

`y = wx + b`

where `x` is your input vector, `w` is your weight vector, `b` is your bias, and `y` is the output.  This can be expanded to matrix representations allowing you to process multiple samples with multiple features and outputs.  This can allow you to simplifiy your code and efficiently process your data using matrix algebra packages.  If you are not familiar with the basics of linear algebra it is probably a good idea to brush up on that, as most of your data will be delivered in and processed as 2D-matrices or their higher-dimensional cousins, tensors.  

Linear representations and techniques form the basis of many algorithms, including [Neural Networks](NeuralNetworks.md) and [Support Vector Machines](SupportVectorMachines.md).  They can be applied to both supervised and unsupervised problems. 

## Linear models of data

In classification, a linear model will identify a line in feature space which allows the bifurcation of space into two parts along a hyperplane.  In regression, the linear model will attempt to plot a line through the points.  

There are many possible ways to do this.  Thus we treat the model (linear) and algorithm separately.  The best goal is to minimize errors.  If however the data is not linearly separable then there is in fact no efficient algorithm for finding optimal setting parameters: it is NP-hard, even to approximately minimize.  This is not such a problem, since minimizing training error would probably be a sign of overfitting and insufficient generalization.  To ensure we do not overfit we introduce a regularizer function in over the parameters in our error calculation to yield a regularized objective.  For a linear model that is `sum(loss(y,wx+b)) + lambda*R(w,b)` where `R` grades the complexity of the solution and `lambda` controls its contribution.

Simple linear models only allow linear boundaries and cannot solve common distributions such as XOR. This can be compensated for by stacking linear models or by feature engineering.  

## Convex surrogate loss functions

Classification commonly is built upon a binary representation where the actual value is 0 or 1 and the predicted value may lie between those numbers.  Optimizing zero-one loss is complicated because it is not smooth and even a small change in value can have a big effect.  A sigmoidal function that smoothly varies between zero and one is potentially easier to optimize but is not convex.  Convex functions are easy to minimize, but non-convex are not.  The four common loss functions are (where `Y` is predicted label):

- Zero/one: `1[yY <= 0]`
- Hinge: `max{0, 1-yY}`
- Logistic: `ln(1+e^-yY)/ln(2)`
- Exponential: `e^-yY`
- Squared: `(y-Y)^2`

## Weight regularization

It is generally a good idea for the weights to remain small.  An easy way to do that is to use the norm, squared norm, or sum of absolute weights of the weight vector. Zero weights are also good, since it means features are not used (and thus you have removed irrelevant features), so sum(1[x <> 0])

This leads to the general concept of p-norms where `||w||p = sum(|w|^p)^(1/p)`.  Changing the value of p interpolates from a star (p<1) to diamond(p=1) to circle(p=2) to square(p=inf).  Small p values prefer sparser vectors, but p<1 the norm is non-convex.  So 1-norm (sum of absolutes) is popular when sparsity is desired.  

## Gradient descent optimization

If you can calculate a gradient at each point then you can take a step in the direction of the gradient of a given size.  The idea is to find the global minimum of the function, which is why convexity is so important (without it gradients do not help you).  The gradient may be found by computing derivatives or where that is not possible sampling the function to find the slope.  When the function is non-differentiable (e.g. hinge) it is often possible to use subgradients.  

When descending a gradient the step size must be chosen to behave appropriately.  There are methods for this.  

Convergence should be detected when the objective function stops changing, the parameters changing, or stopping when test data performance has plateaued.  

## Solving linear equations analytically

Gradient descent is a decent generic approach but in some cases the optimum has a closed form solution that does not require iteration.  This is true of 2-norm regularizer and squared error loss.  To find the answer you need to write this in terms of matrix operations, and solve with linear regression.  

- a = `Xw`
- so `min L(w) = (1/2)||Xw-Y||^2 + (lambda/2)||w||^2`
- solve `w = (trans(X)X + lambda*I)^-1 * trans(X)Y`

If you need to run many iterations in gradient descent then the closed form solution will be faster.  So for low and medium dimensional problems you should favor closed form.

# Perceptron

A percepton is a simple way to find weights for features `f(x) = 1 if wx + b > 0 else 0`, where `wx` is the dot product of the input vector and the weight vector and `b` is the constant bias.  The weight vector is incrementally updated with each example.  The learning set must be linearly separable for it to work. Essentially it is learning a hyperplane classifier, or a linear decision boundary.  

The perceptron has the advantage of being an online algorithm – it can be continuously updated as new data arrives, and only processes one sample at a time.  It is also error driven, and does not update if not necessary (which allows for windowing variants and data set change detection).  However, this means the perceptron tends to favor the most recent examples and forget older ones, and for some data sets may never converge.  Variations of the perceptron can compensate for this by remembering how long a given solution worked.  In theory the perceptron could be run continuously on a stream of data, provided the stream was random and did not have hidden patterns (clusters of label).  

For our purposes we will focus on

1.	Set the weights `w` and `b` = 0
2.	Iterate up to a maximum level:
  1.	Permute examples
  2.	For each example `x` and label `y` (-1 or 1):
    1.	Compute `activation = sum(wd*xd) + b`
    2.	If `y*a <= 0` then `W <- w + yx` else `B <- b + y`
    3.	Normalize w to 1 and adjust b.
3.	Yield `w` and `b` for testing

The algorithm will have converged if a complete run through the training set correctly classifies every point; the data is therefore linearly separable.  Not every training set will converge.  Generally it will converge faster with large margin, but it does not converge on the maximum margin solution.

The only hyperparameter is the number of iterations.  Too many leads to overfitting; tracking the test error may allow you to know when to stop.  Also, the examples should be presented out of order with each iteration.  
