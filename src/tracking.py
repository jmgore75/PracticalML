import pandas as pd
import numpy as np
import time
import datetime
import sys

import os.path
import os
import logging
import weakref
import hashlib
import numbers

from sklearn.externals import joblib
from sklearn import cross_validation
from preprocessors import preprocessors, no_params


class DataAndHash:
    __slots__ = ["hash", "data", "__weakref__"]

    def __init__(self, hash, data):
        self.hash = hash
        self.data = data

    def astuple(self):
        return (self.hash, self.data)


class RunTracker:
    def __init__(self, path):
        self.path = path
        self.inputPath = os.path.join(self.path, "input")
        self.outputPath = os.path.join(self.path, "output")
        self.run_columns = [
            "run_hash", "model", "cv_score", "train_score",
            "samples", "train_samples", "cv_samples",
            "train_time", "score_time",
            "model_bytes", "timestamp"]
        self.runs_file = os.path.join(self.path, "runs.pkl")
        self.best_file = os.path.join(self.path, "bestmodel.pkl")
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if os.path.isfile(self.runs_file):
            self.runs = joblib.load(self.runs_file)
            maxidx = self.runs["cv_score"].idxmax()
            self.max_score = self.runs["cv_score"][maxidx]
            self.best_model = self.runs["model"][maxidx]
            self.best_model_type = self.runs["model_type"][maxidx]
        else:
            self.runs = pd.DataFrame(columns=self.run_columns)
            self.max_score = 0

        self.input_cache = weakref.WeakValueDictionary()
        self.logger = logging.getLogger(self.path)

    def setData(self, X, y, classifier=True):
        X_data = self.hashAndStoreData("X", X)

        y_data = None
        if y is not None:
            y_data = self.hashAndStoreData("y", y)
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
        X_hash, X = self.getData(parent_name).astuple()
        y_hash, y = self.getData("y").astuple()
        self.logger.debug("Generating " + name)
        proc_data = prep.fit_transform(X, y)

        if proc_data:
            data = self.hashAndStoreData(name, proc_data)
            self.logger.debug("Generated " + name)
            return data

        raise NameError("Data not generated for " + name)

    def loadData(self, name):
        if name in self.input_cache:
            data = self.input_cache[name]
            if data:
                return data

        path = os.path.join(self.inputPath, name + ".pkl")
        if os.path.isfile(path):
            data = joblib.load(path)

        if data:
            data = DataAndHash(*data)
            self.cacheData(name, data)
            return data

    def cacheData(self, name, data):
        self.input_cache[name] = data

    def hashAndStoreData(self, name, proc_data):
        if (isinstance(proc_data, np.ndarray) and proc_data.flags.writeable):
            proc_data.flags.writeable = False
        data_hash = hashlib.md5(proc_data.data).hexdigest()
        data = DataAndHash(data_hash, proc_data)
        if not os.path.isdir(self.inputPath):
            os.path.makedirs(self.inputPath)
        path = os.path.join(self.inputPath, name + ".pkl")
        joblib.dump(data.astuple(), path, 1)
        self.cacheData(name, data)
        return data

    def log_run(self, model, run):
        cv_score = run["cv_score"]
        train_time = run["train_time"]
        self.logger.info(run["model"])
        if cv_score >= self.max_score:
            self.logger.warning(
                "Better model %.3f >= %.3f : %.1f s",
                cv_score, self.max_score, train_time)
            self.max_score = cv_score
            self.best_model = run["model"]
            self.best_model_type = run["model_type"]
            #joblib.dump(model, self.best_file, 1)
        else:
            self.logger.warning(
                "Lesser model %.3f <  %.3f : %.1f s",
                cv_score, self.max_score, train_time)
        self.runs = self.runs.append(run, ignore_index=True)
        joblib.dump(self.runs, self.runs_file, 1)

    def make_splits(self, num_points, splits):
        if not splits:
            splits = 1

        if isinstance(splits, numbers.Number):
            splits = cross_validation.ShuffleSplit(num_points, splits, 0.2)

        if hasattr(splits, '__call__'):
            splits = splits(num_points)

        return list(splits)

    def run_models(self, model_gen, splits):
        for model, param_set, mtype in model_gen:
            for run in self.run_model(model, mtype, param_set, splits):
                yield run

    def run_model(self, model, mtype, test_params, splits):
        X_data = self.getData("X")
        y_data = self.getData("y")

        splits = self.make_splits(len(X_data.data), splits)

        if not test_params or not len(test_params):
            test_params = no_params

        for params in test_params:
            model.set_params(**params)
            for i_train, i_cv in splits:
                try:
                    yield self.run_one(model, mtype, X_data, y_data, i_train, i_cv)
                except KeyboardInterrupt:
                    self.logger.warning("Run interrupted: \n" + str(model))
                    raise
                except Exception:
                    self.logger.exception("Run failed: \n" + str(model))

    def run_one(self, model, mtype, X_data, y_data, i_train, i_cv):
        X_hash, X = X_data.astuple()
        y_hash, y = y_data.astuple()

        X_train = X[i_train]
        y_train = y[i_train]
        X_cv = X[i_cv]
        y_cv = y[i_cv]

        run = {}
        run["timestamp"] = datetime.datetime.now().isoformat()
        run["samples"] = len(X)
        run["train_samples"] = len(i_train)
        run["cv_samples"] = len(i_cv)
        model_desc = repr(model.get_params())
        run["model"] = model_desc
        run["model_type"] = mtype

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
        m.update(i_train)
        m.update(i_cv)
        run["run_train_hash"] = m.hexdigest()
        run["model_bytes"] = sys.getsizeof(model)
        self.log_run(model, run)
        return run
