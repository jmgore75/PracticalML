import pandas as pd
import time
import datetime
import sys

import os.path
import os
import logging
import matplotlib.pyplot as plt

#from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib

class TrainingTracker:
    def __init__(self, path, X, y):
        self.path = path
        self.score_file = os.path.join(self.path, "scores.csv")
        self.best_file = os.path.join(self.path, "bestmodel.pkl")
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if os.path.isfile(self.score_file):
            self.scores = pd.read_csv(self.score_file)
            self.max_score = self.scores["test_score"].max()
        else:
            self.scores =
            self.max_score =
        self.X = X
        self.y = y
        self.num_points = len(X)
        self.num_features = #TODO fix this
        self.num_classes =
        self.logger = logging.getLogger(path)

    def standard_clfs(self):
        yield
        yield nolearn()

    def train_suite(self, clfs):
        for clf in clfs:
            train(clf)

    def log_run(self, clf, run):
        run["model"] = clf.__name__
        run["params"] = clf.get_params(true)
        run["model_bytes"] = sys.getsizeof(clf)
        run["timestamp"] = datetime.now().isoformat()

        test_score = run["test_score"]
        train_time = run["train_time"]
        if (test_score >= self.max_score) {
            self.logger.warning("Better model %.3f >= %.3f : %.1f s", test_score, self.max_score, train_time)
            self.max_score = test_score
            joblib.dump(clf, self.best_file)
            performance = "Better"
        } else {
            self.logger.warning("Lesser model %.3f <  %.3f : %.1f s", test_score, self.max_score, train_time)
        }
        self.logger.info(clf)
        self.scores.append(run)
        self.scores.to_csv(self.score_file)

    def plot_run(self, run):
        plt.figure()
        for model, grp in self.scores.groupby(['model']):
            plt.plot(grp['train_time'], grp['test_score'], 'o', label=model)
        plt.plot(run["train_time"], run["test_score"], '*', color="y", s=50, label="Latest")
        plt.xlabel("Train time")
        plt.ylabel("Test score")
        plt.title('Last: %.3f; Best: %.3f' % (grp['test_score'], self.max_score))
        plt.legend(loc="best")
        plt.show()

    def train (self, clf):
        run = {}
        t0 = time.time()
        clf.fit(self.X_train, self.y_train)
        t1 = time.time()
        run["train_score"] = clf.score(self.X_train, self.y_train)
        run["test_score"] = tclf.score(self.X_test, self.y_test)
        t2 = time.time()

        run["train_time"] = t1 - t0
        run["score_time"] = t2 - t1

        run["train_complete"] =
        self.log_run(clf, run)
        return run
