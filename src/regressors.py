from sklearn import linear_model, ensemble, neighbors, svm, kernel_ridge, tree, naive_bayes, lda, qda
from sknn.mlp import Regressor, Layer

def basic_models(n_iter=50):
    yield linear_model.LinearRegression()
    yield linear_model.Ridge(alpha=0.1)
    yield linear_model.Lasso(alpha = 0.1)

def tree_models(n_estimators=[16,64,256,1024]):
    yield tree.DecisionTreeRegressor()
    for n in n_estimators:
        yield ensemble.RandomForestRegressor(n_jobs=-1, n_estimators:n)
        yield ensemble.ExtraTreesRegressor(n_jobs=-1, n_estimators:n)
        yield ensemble.AdaBoostRegressor(n_jobs=-1, n_estimators:n)

def knn_models(n_neighbors=[1, 3, 5, 7]):
    for n in n_neighbors:
        yield neighbors.KNeighborsRegressor(n_neighbors=n)

def svc_models(max_iter=2000):
    yield svm.SVR(kernel='rbf', max_iter=max_iter)
    yield svm.LinearSVR(max_iter=max_iter)
    yield svm.SVR(kernel='poly', degree=2, max_iter=max_iter)
    yield svm.SVR(kernel='sigmoid', C=20, max_iter=max_iter)

def kernel_models(max_iter=2000):
    yield kernel_ridge.KernelRidge(kernel='rbf', max_iter=max_iter)
    yield kernel_ridge.KernelRidge(kernel='linear', max_iter=max_iter)
    yield kernel_ridge.KernelRidge(kernel='sigmoid', max_iter=max_iter)
    yield kernel_ridge.KernelRidge(kernel='poly', max_iter=max_iter)

def nn_models(n_iter=400):
    yield Regressor(
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
        verbose=True)
    yield Regressor(
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
        verbose=True)
    yield Regressor(
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
        verbose=True)

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
