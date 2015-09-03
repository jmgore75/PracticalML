from sklearn import linear_model, ensemble, neighbors, svm, kernel_ridge
from sklearn import tree, grid_search
from sknn.mlp import Regressor, Layer
from sklearn.pipeline import Pipeline

from preprocessors import whiten, lda, scale, no_params


def basic_models(n_iter=50):
    clf = ('linear', linear_model.LinearRegression())
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([lda, clf]), no_params

    clf = ('ridge', linear_model.Ridge(alpha=0.1, tol=1e-2, solver="lsqr"))
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([lda, clf]), no_params

    clf = ('lasso', linear_model.Lasso(alpha=0.1))
    yield Pipeline([whiten, clf]), no_params
    yield Pipeline([lda, clf]), no_params


def tree_models():
    yield tree.DecisionTreeRegressor(), no_params
    param_sets = grid_search.ParameterGrid(
        {"n_estimators": [16, 64, 256, 1024]})
    yield ensemble.RandomForestRegressor(n_jobs=-1), param_sets
    yield tree.DecisionTreeRegressor(n_jobs=-1), param_sets
    yield ensemble.AdaBoostRegressor(n_jobs=-1), param_sets


def knn_models():
    param_sets = grid_search.ParameterGrid({"knn__n_neighbors": [1, 3, 5, 7]})
    knn = ('knn', neighbors.KNeighborsRegressor())
    yield Pipeline([scale, knn]), param_sets
    yield Pipeline([whiten, knn]), param_sets


def svc_models():
    param_sets = [
        {"svr__kernel": "rbf", "svr__C": 1},
        {"svr__kernel": "sigmoid", "svr__C": 20},
        {"svr__kernel": "poly", "svr__degree": 2, "svr__C": 1}]
    yield Pipeline(
        [whiten, ('linear_svr', svm.LinearSVR(max_iter=2000))]), no_params
    yield Pipeline([whiten, ('svr', svm.SVR(max_iter=2000))]), param_sets


def kernel_models(max_iter=2000):
    param_sets = grid_search.ParameterGrid(
        {"kernel__kernel": ['rbf', 'linear', 'sigmoid', 'poly']})
    yield Pipeline([
        whiten,
        ('kernel', kernel_ridge.KernelRidge(max_iter=2000, degree=2))
        ]), param_sets


def nn_models(n_iter=400):
    yield Pipeline([whiten, ('relu2', Regressor(
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
        verbose=True))]), no_params
    yield Pipeline([whiten, ('relu1', Regressor(
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
        verbose=True))]), no_params
    yield Pipeline([whiten, ('sig1', Regressor(
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
        verbose=True))]), no_params


def starting_models():
    for model in basic_models():
        yield model

    for model in knn_models():
        yield model

    for model in tree_models():
        yield model

    for model in svc_models():
        yield model

    for model in kernel_models():
        yield model

    for model in nn_models():
        yield model
