from sklearn import linear_model, ensemble, neighbors, svm, tree
from sklearn import naive_bayes, lda, qda, grid_search
from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline

from preprocessors import scale, no_params, kmeans


def basic_models():
    clf = ('logistic', linear_model.LogisticRegression())
    param_sets = grid_search.ParameterGrid({
        "logistic__class_weight": ["auto", None]})
    yield Pipeline([scale, clf]), param_sets
    yield Pipeline([scale, kmeans, clf]), param_sets

    clf = ('ridge', linear_model.RidgeClassifier(tol=1e-2, solver="lsqr"))
    param_sets = grid_search.ParameterGrid({
        "ridge__class_weight": ["auto", None]})
    yield Pipeline([scale, clf]), no_params
    yield Pipeline([scale, kmeans, clf]), param_sets

    param_sets = grid_search.ParameterGrid({
        "perceptron__class_weight": ["auto", None]})
    clf = ('perceptron', linear_model.Perceptron(n_iter=50))
    yield Pipeline([scale, clf]), param_sets
    yield Pipeline([scale, kmeans, clf]), param_sets

    clf = (
        'passive_aggressive',
        linear_model.PassiveAgressiveClassifier(n_iter=50))
    yield Pipeline([scale, clf]), no_params

    yield lda.LDA(solver='eigen', shrinkage='auto'), no_params

    clf = ('qda', qda.QDA())
    yield Pipeline([scale, clf]), no_params

    yield naive_bayes.GaussianNB(), no_params


def tree_models():
    yield tree.DecisionTreeClassifier(), no_params
    param_sets = grid_search.ParameterGrid({
        "n_estimators": [256, 1024],
        "class_weight": ["subsample", None]})
    yield ensemble.RandomForestClassifier(n_jobs=-1), param_sets
    yield ensemble.ExtraTreesClassifier(n_jobs=-1), param_sets
    yield ensemble.AdaBoostClassifier(), param_sets


def knn_models():
    param_sets = grid_search.ParameterGrid({"knn__n_neighbors": [1, 3, 5, 7]})
    knn = ('knn', neighbors.KNeighborsClassifier())
    yield Pipeline([scale, knn]), param_sets


def svc_models():
    param_sets = grid_search.ParameterGrid([
        {"svc__kernel": "rbf", "svc__class_weight": ["auto", None]},
        {"svc__kernel": "poly", "svc__degree": 2,
            "svc__class_weight": ["auto", None]}])
    yield Pipeline([scale, ('svc', svm.SVC(max_iter=2000))]), param_sets


def nn_models():
    yield Pipeline([scale, ('relu2', Classifier(
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
    yield Pipeline([scale, ('relu1', Classifier(
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
    yield Pipeline([scale, ('sig1', Classifier(
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
    for model, params in tree_models():
        yield model, params

    for model, params in nn_models():
        yield model, params

    for model, params in svc_models():
        yield model, params

    for model, params in basic_models():
        yield model, params

    for model, params in knn_models():
        yield model, params
