from sklearn import linear_model, ensemble, neighbors, svm, kernel_ridge, tree, naive_bayes, lda, qda
from sknn.mlp import Classifier, Layer

def basic_models(n_iter=50):
    yield linear_model.LogisticRegression(penalty="l1"), "whitened"
    yield linear_model.LogisticRegression(penalty="l2"), "whitened"
    yield linear_model.RidgeClassifier(tol=1e-2, solver="lsqr"), "whitened"
    yield linear_model.Perceptron(n_iter=n_iter), "whitened"
    yield linear_model.PassiveAgressiveClassifier(n_iter=n_iter), "whitened"
    yield linear_model.LogisticRegression(penalty="l1"), "lda"
    yield linear_model.LogisticRegression(penalty="l2"), "lda"
    yield linear_model.RidgeClassifier(tol=1e-2, solver="lsqr"), "lda"
    yield linear_model.Perceptron(n_iter=n_iter), "lda"
    yield linear_model.PassiveAgressiveClassifier(n_iter=n_iter), "lda"
    yield lda.LDA(solver='eigen', shrinkage='auto')
    yield qda.QDA(), "scaled"
    yield qda.QDA(), "whitened"
    yield naive_bayes.GaussianNB()

def tree_models(n_estimators=[16,64,256,1024]):
    yield tree.DecisionTreeClassifier()
    for n in n_estimators:
        yield ensemble.RandomForestClassifier(n_jobs=-1, n_estimators:n)
        yield ensemble.ExtraTreesClassifier(n_jobs=-1, n_estimators:n)
        yield ensemble.AdaBoostClassifier(n_jobs=-1, n_estimators:n)

def knn_models(n_neighbors=[1, 3, 5, 7]):
    for n in n_neighbors:
        yield neighbors.KNeighborsClassifier(n_neighbors=n), "scaled"
        yield neighbors.KNeighborsClassifier(n_neighbors=n), "whitened"

def svc_models(max_iter=2000):
    yield svm.SVC(kernel='rbf', max_iter=max_iter), "whitened"
    yield svm.LinearSVC(max_iter=max_iter), "whitened"
    yield svm.SVC(kernel='sigmoid', C=20, max_iter=max_iter), "whitened"
    yield svm.SVC(kernel='poly', degree=2, max_iter=max_iter), "whitened"

def nn_models(n_iter=400):
    yield Classifier(
        layers=[
            Layer("Rectifier", name="fc0", units=100),
            Layer("Rectifier", name="fc1", units=100),
            Layer("Softmax")
        ],
        learning_rate=0.01,
        learning_rule='momentum',
        learning_momentum=0.9,
        batch_size=250,
        valid_size=0.1,
        n_stable=20,
        n_iter=n_iter,
        verbose=True), "whitened"
    yield Classifier(
        layers=[
            Layer("Rectifier", name="fc0", units=100),
            Layer("Softmax")
        ],
        learning_rate=0.01,
        learning_rule='momentum',
        learning_momentum=0.9,
        batch_size=250,
        valid_size=0.1,
        n_stable=20,
        n_iter=n_iter,
        verbose=True), "whitened"
    yield Classifier(
        layers=[
            Layer("Sigmoid", name="fc0", units=100),
            Layer("Softmax")
        ],
        learning_rate=0.01,
        learning_rule='momentum',
        learning_momentum=0.9,
        batch_size=250,
        valid_size=0.1,
        n_stable=20,
        n_iter=n_iter,
        verbose=True), "whitened"

def starting_models():
    for model, form in basic_models():
        yield model, form

    for model, form in knn_models():
        yield model, form

    for model in tree_models():
        yield model, form

    for model in svc_models():
        yield model, form

    for model in nn_models():
        yield model, form
