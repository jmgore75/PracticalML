import pandas as pd
import time
import datetime
import sys

import os.path
import os
import logging
import matplotlib.pyplot as plt
import mpld3
import weakref
import hashlib

from sklearn.externals import joblib
from sklearn import cross_validation, preprocessing
from preprocessors import preprocessors, no_params


class TrainingTracker:
    def __init__(self, path, X, y):
        self.path = path
        self.inputPath = os.path.join(self.path, "input")
        self.outputPath = os.path.join(self.path, "output")
        self.score_columns = [
            "repr", "model", "params", "train_score",
            "test_score", "train_time", "train_complete",
            "score_time", "model_bytes", "timestamp"]
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

        self.input_cache = {}
        self.logger = logging.getLogger(self.path)

    def setData(self, X, y, classifier=True):
        self.num_points = len(X)
        self.feature_names = X.columns
        self.splits = cross_validation.ShuffleSplit(self.num_points, 3, 0.1)
        X_data = self.hashAndStoreData("X", X)

        y_data = None
        if y:
            if classifier:
                labels = preprocessing.LabelBinarizer()
                labels.fit(y)
                self.labels = labels.classes_
            y_data = self.hashAndStoreData("y", y)
            # TODO weights
        return X_data, y_data

    def getData(self, name):
        data = self.loadData(name)
        if data:
            return data
        i = name.rfind("_", -1)
        if i < 0:
            raise NameError(name + " is not available")
        parent_name = name[:i]
        step_name = name[i+1:]
        if not step_name:
            raise NameError("Bad name " + name)
        if step_name not in preprocessors:
            raise NameError("Bad step" + step_name)
        prep = preprocessors[step_name]
        X_hash, X = self.getData(parent_name)
        y_hash, y = self.getData("y")
        self.logger.debug("Generating " + name)
        proc_data = prep.fit_transform(X, y)

        if proc_data:
            data = self.hashAndStoreData(name, proc_data)
            self.logger.debug("Generated " + name)
            return data

        raise NameError("Data not generated for " + name)

    def loadData(self, name):
        if name in self.input_cache:
            data = self.input_cache[name]()
            if data:
                return data

        path = os.path.join(self.inputPath, name + ".pkl")
        if os.path.isfile(path):
            data = joblib.load(path)

        if data:
            self.cacheData(name, data)
            return data

    def cacheData(self, name, data):
        self.input_cache[name] = weakref.ref(data)

    def hashAndStoreData(self, name, proc_data):
        data_hash = hashlib.md5(proc_data).hexdigest()
        data = (data_hash, proc_data)
        if not os.path.isdir(self.inputPath):
            os.path.makedirs(self.inputPath)
        path = os.path.join(self.inputPath, name + ".pkl")
        joblib.dump(data, path)
        self.cacheData(name, data)
        return data

    def log_run(self, model, run):
        test_score = run["test_score"]
        train_time = run["train_time"]
        self.logger.info(run["repr"])
        if test_score >= self.max_score:
            self.logger.warning(
                "Better model %.3f >= %.3f : %.1f s",
                test_score, self.max_score, train_time)
            self.max_score = test_score
            joblib.dump(model, self.best_file)
        else:
            self.logger.warning(
                "Lesser model %.3f <  %.3f : %.1f s",
                test_score, self.max_score, train_time)
        self.scores = self.scores.append(run, ignore_index=True)
        joblib.dump(self.scores, self.score_file)

    def plot_run(self, run):
        from IPython import display
        groups = self.scores.groupby(['model'])
        for model, grp in groups:
            plt.plot(
                grp['train_time'], grp['test_score'],
                'o', label=model)
        if run:
            plt.plot(
                run["train_time"], run["test_score"],
                '*', color="y", s=50, label="Latest")
            plt.title(
                'Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.legend(loc="best")
        plt.figure()

        for model, grp in groups:
            plt.plot(
                grp['train_score'], grp['test_score'],
                'o', label=model)
        if run:
            plt.plot(
                run["train_score"], run["test_score"],
                '*', color="y", s=50, label="Latest")
            plt.title(
                'Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.legend(loc="best")

        mpld3.show()

    def run_models(self, model_gen, cv):
        for model, param_set in model_gen:
            for run in self.run_model(model, param_set, cv):
                yield run

    def run_model(self, model, test_params, cv):
        X_data = self.getData("X")
        y_data = self.getData("y")

        # if not cv or not len(cv):
        #    cv =

        splits = cv

        if not test_params or not len(test_params):
            test_params = no_params

        for params in test_params:
            model.set_params(params)
            for i_train, i_cv in splits:
                try:
                    run = self.run_one(model, X_data, y_data, i_train, i_cv)
                    if run:
                        yield run
                    else:
                        raise  # TODO
                except:
                    self.logger("")

    def run_one(self, model, X_data, y_data, i_train, i_cv):
        X_hash, X = X_data
        y_hash, y = y_data

        X_train = X[i_train]
        y_train = y[i_train]
        X_cv = X[i_cv]
        y_cv = y[i_cv]

        run = {}
        run["timestamp"] = datetime.now().isoformat()
        run["train_samples"] = len(i_train)
        run["cv_samples"] = len(i_cv)
        model_desc = repr(model)
        run["model"] = model_desc

        t0 = time.time()
        model.fit(X_train, y_train)
        t1 = time.time()
        run["train_score"] = model.score(X_train, y_train)
        run["cv_score"] = model.score(X_cv, y_cv)
        t2 = time.time()
        run["train_time"] = t1 - t0
        run["score_time"] = t2 - t1

        m = hashlib.md5()
        m.update(model_desc)
        m.update(X_hash)
        m.update(y_hash)
        run["run_hash"] = m.hexdigest()
        run["model_bytes"] = sys.getsizeof(model)
        self.log_run(model, run)
        return run
