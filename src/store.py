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
            "best": ensemble.ExtraTreesClassifier(n_estimators=250, random_state=0),
            "scaled": preprocessing.StandardScaler(),
            "normalized": preprocessing.Normalizer(),
            "unit": preprocessing.MinMaxScaler(),
            "pca": decomposition.PCA(n_components="mle"),
            "lda": lda.LDA(solver='eigen', shrinkage='auto'),
            "whitened": decomposition.PCA(n_components="mle", whiten=True)
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

    def getData(name):
        data = None
        if name in self.input_cache:
            cache = self.input_cache[name]
            data = cache()
            if data:
                return data

        path = os.path.join(self.inputPath, name + ".pkl")
        if os.path.isfile(path):
            data = joblib.load(path)

        if data:
            self.input_cache[name] = weakref.ref(data)
            return data

        i = name.rfind("_", -1)
        if i < 0:
            raise NameError(name + " is not available")
        parent_name = name[:i]
        step_name = name[i+1:]
        if not step_name:
            raise NameError("Bad name " + name)
        if not step_name in self.preprocessing:
            raise NameError("Bad step" + step_name)
        X = getData(parent_name)
        y = getData("y")
        prep = self.preprocessing[step]
        data = prep.fit_transform(X, y)

        if data:
            self.input_cache[name] = weakref.ref(data)
            if not os.path.isdir(self.inputPath):
                os.path.makedirs(self.inputPath)
            joblib.dump(data, path)
            return data

        raise NameError("Data not generated for " + name)

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

    def train(self, model, prep):
        run = {}
        run["model"] = model.__module__ + "." + model.__class__.__name__
        run["prep"] = prep
        run["repr"] = string(model)
        run["params"] = repr(model.get_params(true))
        run["timestamp"] = datetime.now().isoformat()

        X_name = "X"
        if prep:
            X_name += "_" + prep

        X = self.getData(X_name)
        y = self.getData("y")

        n_split = len(self.splits)
        total_score = 0.0
        train_score = 0.0
        cv_score = 0.0
        train_time = 0.0
        score_time = 0.0
        model_bytes = 0

        for i_train, i_cv in self.splits:
            X_train = X[i_train]
            y_train = y[i_train]
            X_cv = X[i_cv]
            y_cv = y[i_cv]

            t0 = time.time()
            model.fit(X_train, y_train)
            t1 = time.time()
            total_score += model.score(X, y)
            train_score += model.score(X_train, y_train)
            cv_score += model.score(X_cv, y_cv)
            t2 = time.time()
            train_time += t1 - t0
            score_time += t2 - t1
            model_bytes += sys.getsizeof(model)

        run["repr"] = string(model)
        run["params"] = repr(model.get_params(true))
        run["model_bytes"] = sys.getsizeof(model)
        run["total_score"] = total_score / n_split
        run["train_score"] = train_score / n_split
        run["cv_score"] = cv_score / n_split
        run["train_time"] = train_time / n_split
        run["score_time"] = score_time / n_split
        run["model_bytes"] = model_bytes / n_split

        self.log_run(model, run)
        return run
