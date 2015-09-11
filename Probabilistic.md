Probabilistic modeling
=====================

Probabilistic modeling allows you to explicitly think of learning as a problem of statistical inference.  There are two flavors, generative and conditional.  

Generally, models are assuming that there is an unknown probability distribution `D` over input output pairs, i.e. a density function `D = p(x,y)`.  When you have such a function the Bayes optimal classifier is the classifier that returns `y` for `x` that maximizes the value of `D`.  The Bayes error rate is the best you can hope to achieve on this classification problem.  

However you generally do not have this distribution (and even if you did it might not be analytical).  But you can estimate `D`, and use this for classification.  To generate such a probability distribution first select a family of parametric distributions (e.g. Gaussian).  Assume the training data is drawn independently from `D` (which is usually false but true enough).  A useful way to develop probabilistic models is to tell a generative story.  It explains how you believe your training data came into existence.  Then, build your model around that process.  

## Maximum Likelihood Estimation

Find the parameters which maximizes the probability of the observed outcomes.  For coin flips with probability b you would first express the probability of the observations in terms of b and then take the derivative, set it equal to zero, and solve for b.  This gets complicated but solving for the log likelihood is much easier and in this case reduces to the frequency of heads.  

For dice you must maximize prod(p^x) -> sum(x log(p)) with sum(p) = 1.  It is convenient to use lagrange multipliers to enforce the latter constraint, and thus minimize –sum(x log(p)) with sum(p-1) = 0.  Lagrange multiplier adds a new variable lambda to the problem corresponding the constraint, and moves the constraint into the objective.  Thus:

Max lambda min p of – sum(k, x log(p)) – lambda ( sum(k, p-1) )

The trick is that the lagrangian punishes deviations from the constraint very heavily and blows up the objective.  So obeying the constraint is mandatory.

## Naïve Bayes

One issue is that the probability distribution often has a lot of variables (features).  Naïve Bayes assumes that all features are independent conditioned on the label (i.e. if you know the label the probability of any of the features are independent).  As is typical of Bayes, it is flipping the interpretation so that instead of `x -> y`, `y -> p(x)`.  Formally, `p(xd|y,!xd) = p(xd|y)`. Thus

`p(y,x) = p(y) prod(p(xd | y))`

The model for p is a matter of choice and a form of inductive bias which reflects the knowledge of the problem.  

## Graphical Techniques

Graphical techniques have an underlying graph as their model, which represents conditional dependence between random variables.  

Graphs in general can represent any sort of process.  However particular techniques often require particular limitations.  Specifically, a directed acyclic graph (DAG) in which there are no cycles and everything is connected is often required.  

Bayesian Networks are the most popular technique of this kind.  This is a directed acyclic graph (DAG) to which Bayesian logic is applied, such that the probability of all the events is the product of the probability of each event given their parent.  

- Given symptoms, a network to compute the possibilities of various diseases
- Speech signals
- Protein sequences
- Influence diagrams

In a Bayesian network each node is a random variable, the probabilities of which are dependent on the probabilities of the parents.  In a discrete model, this is a simple table of probabilities based on the combined conditions of the parent.  A node is independent of its ancestors given its parents.  The chain rule of probability can then be applied to establish a joint probability of all the nodes.  

For instance, consider the following graph: `C; S | C; R | C; W | S,R`.  Then `P(C,S,R,W) = P(C) * P(S|C) * P(R|C) * P(W|S,R)`.  What we are trying to solve is what those probabilities are. We can calculate the probabilities of parents given their children, and combine these over many examples.

Learning is usually a two-step process:
1. Learn the network structure; `P(G|D) -> P(G)P(D|G) = P(G) int(P(D|G,p)P(p|G)dp`
2. Learn the local distributions implied by the structure

Dynamic Bayesian Networks are graphical models of stochastic proceses.  These can be used for all sorts of networks, such as gene interactions.  Really, they are modeling temporal processes.  A Hidden Markov Model is a simple DBN which has one discrete hidden node and one discrete or continuous observed node per slice, with connections between the hidden nodes.  You are therefore using a sequence of events to predict the underlying process.  Every step depends only on the state of the prior step.  

Note that while the most common Markov chains for modeling are based on only the prior slice it is allowed and often appropriate to model on an arbitrary number of prior slices.  For instance, if one were to use HMM to explain codons in DNA, you might be better served by a 3-HMM.  

- HMM with Gaussian output (observed nodes are Gaussian)
- HMM with mixture of Gaussian output (optional intermediate hidden nodes to Gaussian observed)
- Auto-regressive HMM (observed nodes also depend on prior nodes)
- Factorial HMM (multiple underlying hidden sequences which do not depend on each other)
- Coupled HMM (Parallel HMMs with hidden nodes depending on priors from both chains)
- Input-Output HMM (Observed node also depends on additional observation sequence)
