import pandas as pd
import time
import datetime
import sys

import os.path
import os
import logging
import matplotlib.pyplot as plt
import json
import mpld3
import weakref

#from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib
from sklearn import grid_search
from sklearn import cross_validataion

class TrainingTracker:
    def __init__(self, path, X, y):
        self.path = path
        self.inputPath = os.path.join(self.path, "input")
        self.outputPath = os.path.join(self.path, "output")
        self.score_columns = ["repr", "model", "params", "train_score", "test_score", "train_time", "train_complete", "score_time", "model_bytes", "timestamp"]
        self.score_file = os.path.join(self.path, "scores.pkl")
        self.best_file = os.path.join(self.path, "bestmodel.pkl")
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if os.path.isfile(self.score_file):
            self.scores = joblib.load(self.score_file)
            self.max_score = self.scores["test_score"].max()
        else:
            self.scores = pd.DataFrame(columns=self.score_columns)
            self.max_score = 0

        self.preprocessing = {
            "scaled": preprocessing.StandardScaler(),
            "normalized": preprocessing.Normalizer(),
            "unit": preprocessing.MinMaxScaler(),
            "pca": decomposition.PCA(),
            "whitened": decomposition.PCA #TODO preprocessing for whitened
        }

        self.input_cache = {}
        self.logger = logging.getLogger(self.path)

    def setData(X, y, classifier=True):
        if not os.path.isdir(self.inputPath):
            os.path.makedirs(self.inputPath)

        self.num_points = len(X)
        self.feature_names = X.
        self.splits = cross_validation.ShuffleSplit(self.num_points, 3, 0.1)
        X_path = os.path.join(self.inputPath, "X.pkl")
        joblib.dump(X, X_path)
        self.input_data["X"] = X

        if y:
            if classifier:
                labels = preprocessing.LabelBinarizer()
                labels.fit(y)
                self.labels = labels.classes_
            y_path = os.path.join(self.inputPath, "y.pkl")
            joblib.dump(y, y_path)
            self.input_data["y"] = y

    def getX(preprocessing):
        if preprocessing:
            name = "X_" + preprocessing
        else:
            name = "X"
        path = os.path.join(self.inputPath, name + ".pkl")

        data = None
        if name in self.input_cache:
            cache = self.input_cache[name]
            data = cache()

        if not data:
            if os.path.isfile(path):
                data = joblib.load(path)
            elif preprocessing:
                preprocessor = self.preprocessing[preprocessing]
                data = preprocessor.fit_transform(self.getX())
                if not os.path.isdir(self.inputPath):
                    os.path.makedirs(self.inputPath)
                joblib.dump(data, path)
            else:
                raise NameError(name + " is not available")

        self.input_cache[name] = weakref.ref(data)
        return data

    def log_run(self, model, run):
        test_score = run["test_score"]
        train_time = run["train_time"]
        self.logger.info(run["repr"])
        if test_score >= self.max_score:
            self.logger.warning("Better model %.3f >= %.3f : %.1f s", test_score, self.max_score, train_time)
            self.max_score = test_score
            joblib.dump(model, self.best_file)
        else:
            self.logger.warning("Lesser model %.3f <  %.3f : %.1f s", test_score, self.max_score, train_time)
        self.scores = self.scores.append(run, ignore_index=True)
        joblib.dump(self.scores, self.score_file)

    def plot_run(self, run):
        from IPython import display
        groups = self.scores.groupby(['model'])
        for model, grp in groups:
            plt.plot(grp['train_time'], grp['test_score'], 'o', label=model)
        if run:
            plt.plot(run["train_time"], run["test_score"], '*', color="y", s=50, label="Latest")
            plt.title('Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.legend(loc="best")
        plt.figure()

        for model, grp in groups:
            plt.plot(grp['train_score'], grp['test_score'], 'o', label=model)
        if run:
            plt.plot(run["train_score"], run["test_score"], '*', color="y", s=50, label="Latest")
            plt.title('Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.legend(loc="best")

        mpdl3.show()

    def train_grid(self, model, param_grid):
        for params in grid_search.ParameterGrid(param_grid):
            model.set_params(params)
            self.train(model)

    def train_sample(self, model, param_distributions, n_iter):
        for params in grid_search.ParameterSampler(param_distributions, n_iter):
            model.set_params(params)
            self.train(model)

    def train(self, model):
        run = {}
        run["model"] = model.__module__ + "." + model.__class__.__name__
        run["repr"] = string(model)
        run["params"] = repr(model.get_params(true))
        run["timestamp"] = datetime.now().isoformat()

        X = self.X
        y = self.y
        run["input"] = "raw"

        X_train = X[]
        y_train = y[]
        X_cv = X[]
        y_cv = y[]

        t0 = time.time()
        model.fit(X, y)
        t1 = time.time()
        run["total_score"] = model.score(X, y)
        run["train_score"] = model.score(X_train, y_train)
        run["cv_score"] = model.score(X_cv, y_cv)
        t2 = time.time()
        run["train_time"] = t1 - t0
        run["score_time"] = t2 - t1

        run["repr"] = string(model)
        run["params"] = repr(model.get_params(true))
        run["model_bytes"] = sys.getsizeof(model)

        self.log_run(model, run)
        return run
