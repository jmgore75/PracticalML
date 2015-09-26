Neural networks
===============

A neural network if fundamentally a process which succesively transforms an input through a series of layers until it yields the desired output.  Each layer is fairly simple.  First it performs a linear transformation of its inputs to its outputs (each neuron's output is a weighted sum of the inputs plus a bias).  Then the outputs are transformed with an activation function, so that the end result is non-linear.  These outputs are then passed to the next layer. The non-linear transformation is essential, since a linear transformation followed by a linear transformation is just another linear transformation.  

There are many hyperparameters to choose from with neural networks:

- How many layers to use and in what pattern
- For each layer:
  - the number of units
  - The activation function
  - Which inputs each neuron may use
- The cost function (to control overfitting)
- The choice of learning algorithm

By stacking layer upon layer, very complex transformations of the data can be described.  The core neural network architecture is highly flexible, and can accommodate specialized types of layers such as convolutions, and more complex data flows than simple pipelines.  The state-of-the-art for neural networks is progressing rapidly, with newer and better variations all the time.  

Fundamentally a neural network is a particular type of directected acyclic graph (a layered one).  It is perfectly possible to use a non-layered design and in fact not particularly complex to code.  

## Training neural networks

Training a neural network usually uses a technique called backpropagation.  This is typically done in batches, but could be done with all samples at once or only one sample.  The samples in the batch are first run through the network to produce predictions, keeping track of the calculated activations on each layer.  These predictions are then subtracted from the expected values to generate an error.  

The network is then run backwards.  Using the gradient of the cost function, the error at one layer is distributed to the nodes of the previous layer, and used to calculate a gradient.  The weights of the network are then adjusted using the learning algorithm.  This process is repeated to gradually improve the quality of the prediction.  

## Deep Neural Networks

It has been mathematically demonstrated that one hidden layer, if sufficiently wide, can approximate any function.  However, multiple layers can approximate many functions much more efficiently, and furthermore the nodes in the deeper layers are associated with high-level patterns.  Thus deep neural networks have become

Historically deep neural networks could not be easily trained due to the disappearing gradient issue, where the error could not be backpropagated more than a few of layers without dissipating.  Recently however there have been a series of innovations that have largely solved that issue, particularly the use of rectification as an activation function and the dropout technique.  State-of-the-art neural networks for tasks like image recognition are now massive in size. The chief obstacle to deep learning now is mainly computational power, as the most powerful networks are massive in size.  

### Convolutional Layers

Many features sets have an intrinsic structure or relationships.  Consider a black-and-white image.  It is fundamentally a collection of pixels.  The pixels are all similar to each other - they can take a value in the same range.  Pixels also have a defined neighborhood of other pixels.  Convolutional layers exploit this regularity by using one set of weights to process all of the neighborhoods in the input.  Furthermore, the output of a convolutional layer retains the dimensional structure of the input, which allows the convolutions to be layered effectively.  Each feature learned by a convolution often has an interpretable meaning: shallow layers will learn basic image features like edges, while the deeper layers will learn progressively more sophisticated patterns.  

By taking locality into account, convolutional networks can easily focus in on the content of the input in a way that other algorithms cannot.  They have proven themselves to be extremely powerful where applicable, and currently dominate the image processing space.  

Recently, research has found ways of deconstructing deep convolutional neural networks, allowing them to be enhanced and guided in interesting ways.  Google's [DeepDream](https://en.wikipedia.org/wiki/DeepDream) is one such famous example.  Using nodes in the network associated with a particular pattern, an input image can be modified to force that pattern to appear in the image.  The results are fascinating (if occasionally disturbing).  More recently, similar research has found ways to [separate content and style](http://arxiv.org/pdf/1508.06576v1.pdf) in the networks, allowing images to be reinterpreted in the style of famous artworks.  

## Recurrent neural networks

Not all data to be processed takes the form of independent samples.  You may be consuming and/or producing streams of samples, such as audio, video, and text.  In that case, the length of the stream may be of unknown size or even indefinite, and how the samples change over time is of fundamental importance.  Your model must therefore possess memory.  

Recurrent neural networks are one of the few documented ways of modeling such data, by allowing state to carry over between steps.  There are many such architectures, but the one most commonly used is the [Long Short-Term Memory](https://en.wikipedia.org/wiki/Long_short_term_memory) architecture.  As RNNs go it is relatively simple but can remember state for an arbitrary length of time.  

## Extreme Learning Machines

Extreme Learning Machines are a variant of neural networks (usually with one relatively large hidden layer).  The input-hidden weights are initialized randomly (like usual).  The hidden-output weights are then calculated analytically (not like usual).  And that's it - no backpropagation necessary.  Amazingly, this comically simple and fast approach works pretty well.  In practice a few rounds of backpropagation will improve the results even more.

Essentially, an extreme learning machine is just a logistic/linear regression, albeit on a random and non-linear transformation of the original features.  The fact that it works, and works well, demonstrates two important things: firstly, that discovering tractable features (through transformation or engineering) is *the* critical task of any machine learning pipeline; secondly, that a random linear transformation of arbitrary features can produce a new set of features tractable to linear analysis.  
