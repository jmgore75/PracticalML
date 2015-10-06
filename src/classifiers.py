from sklearn import linear_model, ensemble, neighbors, svm, tree
from sklearn import naive_bayes, lda, qda, grid_search
from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline

from preprocessors import best, scale, no_params, kmeans


def basic_models():
    clf = ('logistic', linear_model.LogisticRegression())
    param_sets = grid_search.ParameterGrid({
        "logistic__class_weight": ["auto", None]})
    yield Pipeline([best, scale, clf]), param_sets, "Linear"
    yield Pipeline([best, scale, kmeans, clf]), param_sets, "KMeans Linear"

    clf = ('ridge', linear_model.RidgeClassifier(tol=1e-2, solver="lsqr"))
    param_sets = grid_search.ParameterGrid({
        "ridge__class_weight": ["auto", None]})
    yield Pipeline([best, scale, clf]), no_params, "Linear"
    yield Pipeline([best, scale, kmeans, clf]), param_sets, "KMeans Linear"

    param_sets = grid_search.ParameterGrid({
        "perceptron__class_weight": ["auto", None]})
    clf = ('perceptron', linear_model.Perceptron(n_iter=50))
    yield Pipeline([best, scale, clf]), param_sets, "Linear"
    yield Pipeline([best, scale, kmeans, clf]), param_sets, "KMeans Linear"

    clf = (
        'passive_aggressive',
        linear_model.PassiveAggressiveClassifier(n_iter=50))
    yield Pipeline([best, scale, clf]), no_params, "Linear"

    yield lda.LDA(solver='eigen', shrinkage='auto'), no_params, "Other"

    clf = ('qda', qda.QDA())
    yield Pipeline([scale, clf]), no_params, "Other"

    yield naive_bayes.GaussianNB(), no_params, "Other"


def tree_models():
    yield tree.DecisionTreeClassifier(), no_params, "DT"
    param_sets = grid_search.ParameterGrid({
        "n_estimators": [100, 400],
        "class_weight": ["subsample", None]})
    yield ensemble.ExtraTreesClassifier(n_jobs=-1), param_sets, "ET"
    yield ensemble.RandomForestClassifier(n_jobs=-1), param_sets, "RF"
#    yield ensemble.AdaBoostClassifier(), param_sets


def knn_models():
    param_sets = grid_search.ParameterGrid({"knn__n_neighbors": [1, 3, 5, 7]})
    knn = ('knn', neighbors.KNeighborsClassifier())
    yield Pipeline([best, scale, knn]), param_sets, "KNN"


def svc_models():
    param_sets = grid_search.ParameterGrid([
        {"svc__kernel": ["rbf"], "svc__class_weight": ["auto", None]},
        {"svc__kernel": ["poly"], "svc__degree": [2],
            "svc__class_weight": ["auto", None]}])
    yield Pipeline([best, scale, ('svc', svm.SVC(max_iter=400))]), param_sets, "SVM"


def nn_models():
    yield Pipeline([best, scale, ('relu2', Classifier(
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
        verbose=True))]), no_params, "ANN"
    yield Pipeline([best, scale, ('relu1', Classifier(
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
        verbose=True))]), no_params, "ANN"
    yield Pipeline([best, scale, ('sig1', Classifier(
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
        verbose=True))]), no_params, "ANN"


def starting_models():
    for model, params, mtype in tree_models():
        yield model, params, mtype

    for model, params, mtype in knn_models():
        yield model, params, mtype

    for model, params, mtype in nn_models():
        yield model, params, mtype

    for model, params, mtype in svc_models():
        yield model, params, mtype

    for model, params, mtype in basic_models():
        yield model, params, mtype
