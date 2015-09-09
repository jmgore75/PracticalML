Building your Machine Learning environment
==================================

## Factors in selecting ML environment

When choosing the system to perform machine learning (if you have a choice) you should take the following three aspects into account:

1. Plenty of memory (8GB)
2. NVidia GPU installed (for CUDA) or a decent CPU
3. Prefer Linux

First and foremost, you want memory, for the following reasons:
- Datasets themselves are often large
- Many algorithms have significant working memory requirements, particularly when there are many features (SVM, DNN)
- Pretty much all algorithms with low intrinsic bias improve with more data, so if you can get more you should.  

Running models on the GPU rather than the CPU can massively improve their performance: 30 times speedup is often the case.  This can make a huge difference in your ability to investigate.  

The major machine learning/data science platforms are available on all platforms.  However, a lot of ML libraries are high performance and requires compilation (including dynamic compilation).  Naturally the build process makes a lot of assumptions about particular compilers and libraries being available (even the shell environment).  And they are nearly all open source.  So Linux will generally be your least painful option.  OS X is ok but often requires you to set up a lot of stuff in advance.  The Windows situation is similar, and additionally complicated by its non-unix heritage.  

## Strengths and weaknesses of the major ML platforms:

At the moment, there are four major ML environments: R, Python, MatLab, and Julia.  I have used all four environments at one time or another.  Additionally, there are many C libraries, Java libraries, and services available.  

[R](https://www.r-project.org/) is the premier open source statistical computing and graphics language and environment.  It is also the most popular ML toll and has thousands of packages.  It is widely used in academia and research, and implementations of new algorithms are often delivered in R.  

[Python](https://www.python.org/) is a high-level and flexible general-purpose dynamic programming language.  Most machine learning on python goes through the  [scikit-learn](http://scikit-learn.org) package, which wraps many ML algorithms in a single standard interface along with plenty of processing and analysis tools.  High performance algorithms can be handled by the [Theano](http://deeplearning.net/software/theano) package and any one of several neural network packages.  Python is production ready and is excellent for data wrangling.  For these reasons it is my personal choice.  

[MatLab](http://www.mathworks.com/products/matlab/) is a numerical computing environment with extensive use in academic and research institutions.  It is also proprietary and expensive.  Its open source clone [Octave](https://www.gnu.org/software/octave/) uses the same language but is not nearly as nice.  

[Julia](http://julialang.org/) is a very new high-performance dynamic programming language. It is specifically designed for numerical and scientific computing but also aims to be an effective general purpose language: ["the speed of C with the dynamism of Ruby"](http://julialang.org/blog/2012/02/why-we-created-julia/).  In practice the code is similar to MatLab but with [parametric types](https://en.wikipedia.org/wiki/Parametric_polymorphism).  The performance is actually quite good.  As such it has attracted a lot of interest in the machine learning community and is rapidly developing a package ecosystem.  However it is still early beta and even some core APIs are changing, so I can't recommend it just yet.  
