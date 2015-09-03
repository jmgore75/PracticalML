from sklearn import linear_model, ensemble, neighbors, svm, tree
from sklearn import naive_bayes, lda, qda, grid_search
from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline

from preprocessors import scale, whiten, no_params, lda as plda


def basic_models():
    clf = ('logistic', linear_model.LogisticRegression())
    param_sets = grid_search.ParameterGrid({"logistic__penalty": ["l1", "l2"]})
    yield Pipeline([whiten, clf]), param_sets
    yield Pipeline([plda, clf]), param_sets

    clf = ('ridge', linear_model.RidgeClassifier(tol=1e-2, solver="lsqr"))
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([plda, clf]), no_params

    clf = ('perceptron', linear_model.Perceptron(n_iter=50))
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([plda, clf]), no_params

    clf = (
        'passive_aggressive',
        linear_model.PassiveAgressiveClassifier(n_iter=50))
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([plda, clf]), no_params

    yield lda.LDA(solver='eigen', shrinkage='auto'), no_params

    clf = ('qda', qda.QDA())
    yield Pipeline([scale, clf]), no_params
    yield Pipeline([whiten, clf]), no_params

    yield naive_bayes.GaussianNB(), no_params


def tree_models():
    yield tree.DecisionTreeClassifier(), no_params
    param_sets = grid_search.ParameterGrid({
        "n_estimators": [16, 64, 256, 1024]})
    yield ensemble.RandomForestClassifier(n_jobs=-1), param_sets
    yield tree.DecisionTreeClassifier(n_jobs=-1), param_sets
    yield ensemble.AdaBoostClassifier(n_jobs=-1), param_sets


def knn_models():
    param_sets = grid_search.ParameterGrid({"knn__n_neighbors": [1, 3, 5, 7]})
    knn = ('knn', neighbors.KNeighborsClassifier())
    yield Pipeline([scale, knn]), param_sets
    yield Pipeline([whiten, knn]), param_sets


def svc_models():
    param_sets = [
        {"svc__kernel": "rbf", "svc__C": 1},
        {"svc__kernel": "sigmoid", "svc__C": 20},
        {"svc__kernel": "poly", "svc__degree": 2, "svc__C": 1}]
    yield Pipeline([whiten, ('svc', svm.LinearSVC(max_iter=2000))]), no_params
    yield Pipeline([whiten, ('svc', svm.SVC(max_iter=2000))]), param_sets


def nn_models():
    yield Pipeline([whiten, ('relu2', Classifier(
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
        n_iter=400,
        verbose=True))]), no_params
    yield Pipeline([whiten, ('relu1', Classifier(
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
        n_iter=400,
        verbose=True))]), no_params
    yield Pipeline([whiten, ('sig1', Classifier(
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
        n_iter=400,
        verbose=True))]), no_params


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